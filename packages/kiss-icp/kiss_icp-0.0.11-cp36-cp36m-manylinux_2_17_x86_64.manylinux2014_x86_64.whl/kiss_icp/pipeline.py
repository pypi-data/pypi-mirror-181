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
import datetime
import os
from pathlib import Path
import time
from typing import List

import numpy as np

from kiss_icp.config import KISSConfig, load_config, write_config
from kiss_icp.metrics import absolute_trajectory_error, sequence_error
from kiss_icp.odometry import Odometry
from kiss_icp.tools.pipeline_results import PipelineResults
from kiss_icp.tools.progress_bar import get_progress_bar
from kiss_icp.visualizer import RegistrationVisualizer, StubVisualizer


class OdometryPipeline:
    def __init__(
        self,
        dataset,
        config: Path,
        deskew: bool = False,
        visualize: bool = False,
        n_scans: int = -1,
        jump: int = 0,
    ):
        self._dataset = dataset
        self._n_scans = (
            len(self._dataset) - jump if n_scans == -1 else min(len(self._dataset) - jump, n_scans)
        )
        self._jump = jump
        self._first = jump
        self._last = self._jump + self._n_scans
        self.config: KISSConfig = load_config(config)
        self.config.data = self._dataset.config.data  # TODO(Nacho): Fix this config mess

        # Pipeline
        self.odometry = Odometry(config=self.config, deskew=deskew)
        self.results = PipelineResults()
        self.times = []
        self.poses = self.odometry.poses
        self.has_gt = hasattr(self._dataset, "gt_poses")
        self.gt_poses = self._dataset.gt_poses[self._first : self._last] if self.has_gt else None
        self.dataset_name = self._dataset.__class__.__name__
        self.dataset_sequence = self._dataset.sequence_id

        # Visualizer
        self.visualizer = RegistrationVisualizer() if visualize else StubVisualizer()
        if hasattr(self._dataset, "use_global_visualizer"):
            self.visualizer.global_view = self._dataset.use_global_visualizer

    # Public interface  ------
    def run(self):
        self._run_pipeline()
        self._run_evaluation()
        self._write_result_poses()
        self._write_gt_poses()
        self._write_cfg()
        self._write_log()
        return self.results

    # Private interface  ------
    def _run_pipeline(self):
        for idx in get_progress_bar(self._first, self._last):
            frame, timestamps = self._next(idx)
            start_time = time.perf_counter_ns()
            in_frame, source = self.odometry.register_frame(frame, timestamps)
            self.times.append(time.perf_counter_ns() - start_time)
            self.visualizer.update(in_frame, source, self.odometry.local_map, self.poses[-1])

    def _next(self, idx):
        """TODO: re-arrange this logic"""
        dataframe = self._dataset[idx]
        try:
            frame, timestamps = dataframe
        except ValueError:
            frame = dataframe
            timestamps = np.zeros(frame.shape[0])
        return frame, timestamps

    @property
    def results_dir(self):
        return self._get_results_dir(self.config.out_dir)

    def _write_poses(self, poses: List[np.ndarray], filename: str):
        def _to_kitti_format(poses: np.ndarray) -> np.ndarray:
            return np.array([np.concatenate((pose[0], pose[1], pose[2])) for pose in poses])

        np.savetxt(
            fname=filename,
            X=_to_kitti_format(
                self._dataset.apply_calibration(poses)
                if hasattr(self._dataset, "apply_calibration")
                else poses
            ),
        )

    def _write_result_poses(self):
        self._write_poses(self.poses, f"{self.results_dir}/{self._dataset.sequence_id}.txt")

    def _write_gt_poses(self):
        if not self.has_gt:
            return
        # Dump always (calibrated) gt_poses to disk for re-evaluation
        self._write_poses(self.gt_poses, f"{self.results_dir}/{self._dataset.sequence_id}_gt.txt")

    def _run_evaluation(self):
        if not self.has_gt:
            print("[WARNING] No GT poses available, skipping evaluation")
            return

        def _get_fps():
            total_time_s = sum(self.times) * 1e-9
            return float(len(self.times) / total_time_s)

        # Run metrics evaluation
        avg_tra, avg_rot = sequence_error(self.gt_poses, self.poses)
        ate_rot, ate_trans = absolute_trajectory_error(self.gt_poses, self.poses)
        avg_fps = int(np.floor(_get_fps()))
        avg_ms = 1e3 * (1 / avg_fps)

        self.results.append(desc="Average Translation Error", units="%", value=avg_tra)
        self.results.append(desc="Average Rotational Error", units="deg/m", value=avg_rot)
        self.results.append(desc="Absoulte Trajectory Error (ATE)", units="m", value=ate_trans)
        self.results.append(desc="Absoulte Rotational Error (ARE)", units="rad", value=ate_rot)
        self.results.append(desc="Average Frequency", units="Hz", value=avg_fps, trunc=True)
        self.results.append(desc="Average Runtime", units="ms", value=avg_ms, trunc=True)

    def _write_log(self):
        if not self.results.empty():
            self.results.log_to_file(
                f"{self.results_dir}/result_metrics.log",
                f"Results for {self.dataset_name} Sequence {self.dataset_sequence}",
            )

    def _write_cfg(self):
        write_config(self.config, os.path.join(self.results_dir, "config.yml"))

    @staticmethod
    def _get_results_dir(out_dir: str):
        def get_current_timestamp() -> str:
            return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        results_dir = os.path.join(os.path.realpath(out_dir), get_current_timestamp())
        latest_dir = os.path.join(os.path.realpath(out_dir), "latest")
        os.makedirs(results_dir, exist_ok=True)
        os.unlink(latest_dir) if os.path.exists(latest_dir) else None
        os.symlink(results_dir, latest_dir)
        return results_dir
