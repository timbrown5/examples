# Copyright (c) 2021 Graphcore Ltd. All rights reserved.

import unittest
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).absolute().parent.parent))
from callbacks.throughput_estimator_callback import ThroughputEstimatorCallback


class Mock_time:
    time_step = 10
    counter = 0

    @staticmethod
    def time():
        Mock_time.counter += Mock_time.time_step
        return Mock_time.counter


class ThroughputEstimatorTest(unittest.TestCase):

    @unittest.mock.patch('callbacks.throughput_estimator_callback.time', Mock_time)
    def test_throughput(self):
        steps_per_execution = 2
        micro_batch_size = 2

        callback = ThroughputEstimatorCallback(
            steps_per_execution=steps_per_execution, micro_batch_size=micro_batch_size)

        callback.on_train_begin()
        logs = {}
        callback.on_train_batch_begin(0, logs)
        callback.on_train_batch_end(0, logs)

        self.assertAlmostEqual(logs, {'Average images/s': 0.4})
