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

import natsort
import numpy as np

from kiss_icp.config import KISSConfig, load_config
from kiss_icp.datasets.cache import get_cache, memoize


class BoreasDataset:
    def __init__(
        self,
        data_dir: Path,
        config: Path,
        max_range: Optional[float] = None,
        no_cache: Optional[bool] = None,
        *_,
        **__,
    ):
        self.config = load_config(config)
        self.config.data.max_range = max_range if max_range else self.config.data.max_range
        self.root_dir = os.path.realpath(data_dir)
        self.scan_files = natsort.natsorted(glob.glob(f"{data_dir}/lidar/*.bin"))
        self.gt_poses = self.load_poses(f"{data_dir}/applanix/lidar_poses.csv")
        self.sequence_id = os.path.basename(data_dir)
        assert len(self.scan_files) == self.gt_poses.shape[0]

        # Cache
        self.use_cache = False if no_cache else self.config.use_cache
        self.cache = get_cache(directory=os.path.join(self.__class__.__name__, self.sequence_id))

    def __len__(self):
        return len(self.scan_files)

    def __getitem__(self, idx):
        return self.read_point_cloud(self.scan_files[idx], self.config.data)

    @memoize()
    def read_point_cloud(self, scan_file: str, config: KISSConfig.data):
        points = np.fromfile(scan_file, dtype=np.float32).reshape((-1, 6))[:, :3]
        points = self._preprocess(points, config) if config.preprocess else points
        return points.astype(np.float64), self.get_timestamps(points)

    def load_poses(self, poses_file):
        data = np.loadtxt(poses_file, delimiter=",", skiprows=1)
        n, m = data.shape
        t, x, y, z, vx, vy, vz, r, p, y, wz, wy, wx = data[0, :]
        first_pose = self.get_transformation_matrix(x, y, z, y, p, r)
        poses = np.empty((n, 4, 4), dtype=np.float32)
        poses[0, :, :] = np.identity(4, dtype=np.float32)
        for i in range(n):
            t, x, y, z, vx, vy, vz, r, p, y, wz, wy, wx = data[i, :]
            current_pose = self.get_transformation_matrix(x, y, z, y, p, r)
            poses[i, :, :] = np.linalg.inv(first_pose) @ current_pose
        return poses

    @staticmethod
    def _preprocess(points, config: KISSConfig.data):
        points = points[np.linalg.norm(points, axis=1) <= config.max_range]
        points = points[np.linalg.norm(points, axis=1) >= config.min_range]
        return points

    @staticmethod
    def get_timestamps(points):
        x = points[:, 0]
        y = points[:, 1]
        yaw = -np.arctan2(y, x)
        timestamps = 0.5 * (yaw / np.pi + 1.0)
        return timestamps

    @staticmethod
    def get_transformation_matrix(x, y, z, yaw, pitch, roll):
        T_enu_sensor = np.identity(4, dtype=np.float64)
        R_yaw = np.array(
            [[np.cos(yaw), np.sin(yaw), 0], [-np.sin(yaw), np.cos(yaw), 0], [0, 0, 1]],
            dtype=np.float64,
        )
        R_pitch = np.array(
            [[np.cos(pitch), 0, -np.sin(pitch)], [0, 1, 0], [np.sin(pitch), 0, np.cos(pitch)]],
            dtype=np.float64,
        )
        R_roll = np.array(
            [[1, 0, 0], [0, np.cos(roll), np.sin(roll)], [0, -np.sin(roll), np.cos(roll)]],
            dtype=np.float64,
        )
        C_enu_sensor = R_roll @ R_pitch @ R_yaw
        T_enu_sensor[:3, :3] = C_enu_sensor
        r_sensor_enu_in_enu = np.array([x, y, z]).reshape(3, 1)
        T_enu_sensor[:3, 3:] = r_sensor_enu_in_enu
        return T_enu_sensor
