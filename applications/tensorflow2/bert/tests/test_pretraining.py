# Copyright (c) 2021 Graphcore Ltd. All rights reserved.

from tests.utils import get_app_root_dir
from examples_tests.test_util import SubProcessChecker


class TestBuildAndRun(SubProcessChecker):

    def _get_sample_dataset_path(self):
        app_dir = get_app_root_dir()
        return app_dir.joinpath("data_utils").joinpath("wikipedia").resolve()

    def _get_pretraining_command(self, extra_args=None):
        base_cmd = ("python run_pretraining.py tests/pretrain_tiny_test.json")
        print(f"Running: {base_cmd}")
        if extra_args is not None and len(extra_args) > 0:
            base_cmd += " " + " ".join(extra_args)
        return base_cmd

    def test_run_pretraining(self):
        cmd = self._get_pretraining_command(
            extra_args=["--dataset-dir", str(self._get_sample_dataset_path())])
        self.run_command(cmd,
                         get_app_root_dir(),
                         [""])
