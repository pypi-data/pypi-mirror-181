# MIT License
#
# Copyright (c) 2022 Ignacio Vizzo, Tiziano Guadagnino, Benedikt Mersch, Cyrill
# Stachniss.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import os
from pathlib import Path
import sys
from typing import Optional

import natsort
import numpy as np

from kiss_icp.config import KISSConfig, load_config
from kiss_icp.datasets import supported_file_extensions
from kiss_icp.datasets.cache import get_cache, memoize


class GenericDataset:
    def __init__(
        self,
        data_dir: Path,
        config: Path,
        max_range: Optional[float] = None,
        no_cache: Optional[bool] = None,
        *_,
        **__,
    ):
        # Config stuff
        self.config = load_config(config)
        self.config.data.max_range = max_range if max_range else self.config.data.max_range
        self.sequence_id = os.path.basename(data_dir)
        self.scans_dir = os.path.join(os.path.realpath(data_dir), "")
        self.scan_files = np.array(
            natsort.natsorted(
                [
                    os.path.join(self.scans_dir, fn)
                    for fn in os.listdir(self.scans_dir)
                    if any(fn.endswith(ext) for ext in supported_file_extensions())
                ]
            ),
            dtype=np.str,
        )
        if len(self.scan_files) == 0:
            raise ValueError(f"Tried to read point cloud files in {self.scans_dir} but none found")
        self.file_extension = self.scan_files[0].split(".")[-1]
        if self.file_extension not in supported_file_extensions():
            raise ValueError(f"Supported formats are: {supported_file_extensions()}")

        # Obtain the pointcloud reader for the given data folder
        self._read_point_cloud = self._get_point_cloud_reader()

        # Cache
        self.use_cache = False if no_cache else self.config.use_cache
        self.cache = get_cache(directory=os.path.join(self.__class__.__name__, self.sequence_id))

    def __len__(self):
        return len(self.scan_files)

    def __getitem__(self, idx):
        return self.read_point_cloud(self.scan_files[idx], self.config.data)

    @memoize()
    def read_point_cloud(self, file_path: str, config: KISSConfig.data):
        points = self._read_point_cloud(file_path)
        points = self._preprocess(points, config) if config.preprocess else points
        return points.astype(np.float64)

    @staticmethod
    def _preprocess(points, config: KISSConfig.data):
        points = points[np.linalg.norm(points, axis=1) <= config.max_range]
        points = points[np.linalg.norm(points, axis=1) >= config.min_range]
        return points

    def _get_point_cloud_reader(self):
        """Attempt to guess with try/catch blocks which is the best point cloud reader to use for
        the given dataset folder. Supported readers so far are:
            - np.fromfile
            - trimesh.load
            - PyntCloud
            - open3d[optional]
        """
        # This is easy, the old KITTI format
        if self.file_extension == "bin":
            print("[WARNING] Reading .bin files, the only format supported is the KITTI format")
            return lambda file: np.fromfile(file, dtype=np.float32).reshape((-1, 4))[:, :3]

        print('Trying to guess how to read your data: "pip install kiss-icp[all]" is required')
        first_scan_file = self.scan_files[0]

        # first try trimesh
        try:
            import trimesh

            trimesh.load(first_scan_file)
            return lambda file: np.asarray(trimesh.load(file).vertices)
        except:
            pass

        # then try pyntcloud
        try:
            from pyntcloud import PyntCloud

            PyntCloud.from_file(first_scan_file)
            return lambda file: PyntCloud.from_file(file).points[["x", "y", "z"]].to_numpy()
        except:
            pass

        # lastly with open3d
        try:
            import open3d as o3d

            o3d.io.read_point_cloud(first_scan_file)
            return lambda file: np.asarray(o3d.io.read_point_cloud(file).points, dtype=np.float64)
        except:
            print("[ERROR], File format not supported")
            sys.exit(1)
