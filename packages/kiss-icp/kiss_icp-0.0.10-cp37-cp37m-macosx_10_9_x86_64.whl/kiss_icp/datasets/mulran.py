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

import glob
import os
from pathlib import Path
from typing import Optional

import numpy as np

from kiss_icp.config import KISSConfig, load_config
from kiss_icp.datasets.cache import get_cache, memoize


class MulranDataset:
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
        self.sequence_dir = os.path.realpath(data_dir)
        self.velodyne_dir = os.path.join(self.sequence_dir, "Ouster/")

        # Use this rotation matrix to have a forward looking X axi
        self.R = np.array(  # R.from_euler("xyz", [0.0, 0.0, 180.0])
            [
                [-1.0, -0.0, 0.0, 0.0],
                [0.0, -1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0],
            ]
        )

        self.scan_files = sorted(glob.glob(self.velodyne_dir + "*.bin"))
        self.scan_timestamps = [int(os.path.basename(t).split(".")[0]) for t in self.scan_files]

        # Cache
        self.use_cache = False if no_cache else self.config.use_cache
        self.cache = get_cache(directory=os.path.join(self.__class__.__name__, self.sequence_id))

        # Load poses after cache is created
        self.gt_poses = self.load_gt_poses(os.path.join(self.sequence_dir, "global_pose.csv"))

    def __len__(self):
        return len(self.scan_files)

    def __getitem__(self, idx):
        return self.read_point_cloud(self.scan_files[idx], self.config.data)

    @memoize()
    def read_point_cloud(self, file_path: str, config: KISSConfig.data):
        points = np.fromfile(file_path, dtype=np.float32).reshape((-1, 4))[:, :3]
        points = self.transform_points(points, self.R)
        timestamps = self.get_timestamps()
        if points.shape[0] != timestamps.shape[0]:
            # MuRan has some broken point clouds, just fallback to no timestamps
            return points.astype(np.float64), np.ones(points.shape[0])
        if config.preprocess:
            points, timestamps = self._preprocess(points, timestamps, config)
        return points.astype(np.float64), timestamps

    @staticmethod
    def _preprocess(points, timestamps, config: KISSConfig.data):
        ranges = np.linalg.norm(points, axis=1)
        filter_ = np.logical_and(ranges <= config.max_range, ranges >= config.min_range)
        return points[filter_], timestamps[filter_]

    @staticmethod
    def get_timestamps():
        H = 64
        W = 1024
        return (np.floor(np.arange(H * W) / H) / W).reshape(-1, 1)

    @memoize()
    def load_gt_poses(self, poses_file: str):
        """MuRan has more poses than scans, therefore we need to match 1-1 timestamp with pose"""

        def read_csv(poses_file: str):
            poses = np.loadtxt(poses_file, delimiter=",")
            timestamps = poses[:, 0]
            poses = poses[:, 1:]
            n = poses.shape[0]
            poses = np.concatenate(
                (poses, np.zeros((n, 3), dtype=np.float32), np.ones((n, 1), dtype=np.float32)),
                axis=1,
            )
            poses = poses.reshape((n, 4, 4))  # [N, 4, 4]
            return poses, timestamps

        # Read the csv file
        poses, timestamps = read_csv(poses_file)
        # Extract only the poses that has a matching Ouster scan
        poses = poses[[np.argmin(abs(timestamps - t)) for t in self.scan_timestamps]]

        # Convert from global coordinate poses to local poses
        first_pose = poses[0, :, :]
        poses = np.linalg.inv(first_pose) @ poses

        T_lidar_to_base, T_base_to_lidar = self._get_calibration()
        return T_lidar_to_base @ poses @ T_base_to_lidar

    def _get_calibration(self):
        # Apply calibration obtainbed from calib_base2ouster.txt
        #  T_lidar_to_base[:3, 3] = np.array([1.7042, -0.021, 1.8047])
        #  T_lidar_to_base[:3, :3] = tu_vieja.from_euler(
        #  "xyz", [0.0001, 0.0003, 179.6654], degrees=True
        #  )
        T_lidar_to_base = np.array(
            [
                [-9.9998295e-01, -5.8398386e-03, -5.2257060e-06, 1.7042000e00],
                [5.8398386e-03, -9.9998295e-01, 1.7758769e-06, -2.1000000e-02],
                [-5.2359878e-06, 1.7453292e-06, 1.0000000e00, 1.8047000e00],
                [0.0000000e00, 0.0000000e00, 0.0000000e00, 1.0000000e00],
            ]
        )
        T_lidar_to_base = self.R @ T_lidar_to_base
        T_base_to_lidar = np.linalg.inv(T_lidar_to_base)
        return T_lidar_to_base, T_base_to_lidar

    @staticmethod
    def transform_points(points, matrix, translate=True):
        """
        Taken from: 'from trimesh import transform_points'
        Returns points rotated by a homogeneous
        transformation matrix.

        If points are (n, 2) matrix must be (3, 3)
        If points are (n, 3) matrix must be (4, 4)

        Parameters
        ----------
        points : (n, D) float
          Points where D is 2 or 3
        matrix : (3, 3) or (4, 4) float
          Homogeneous rotation matrix
        translate : bool
          Apply translation from matrix or not

        Returns
        ----------
        transformed : (n, d) float
          Transformed points
        """
        points = np.asanyarray(points, dtype=np.float64)
        # no points no cry
        if len(points) == 0:
            return points.copy()

        matrix = np.asanyarray(matrix, dtype=np.float64)
        if len(points.shape) != 2 or (points.shape[1] + 1 != matrix.shape[1]):
            raise ValueError(
                "matrix shape ({}) doesn't match points ({})".format(matrix.shape, points.shape)
            )

        # check to see if we've been passed an identity matrix
        identity = np.abs(matrix - np.eye(matrix.shape[0])).max()
        if identity < 1e-8:
            return np.ascontiguousarray(points.copy())

        dimension = points.shape[1]
        column = np.zeros(len(points)) + int(bool(translate))
        stacked = np.column_stack((points, column))
        transformed = np.dot(matrix, stacked.T).T[:, :dimension]
        transformed = np.ascontiguousarray(transformed)
        return transformed
