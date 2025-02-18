# Copyright (c) 2021 Graphcore Ltd. All rights reserved.

import unittest
import tensorflow as tf
from tensorflow.python import ipu


class StochasticRounding(unittest.TestCase):

    def run_ipu_prog(self, stochastic_rounding: bool):
        tf.keras.mixed_precision.set_global_policy('float16')

        weight_value = 1000.0
        num_iterations = 250
        gradient_value = 1e-1

        strategy = ipu.ipu_strategy.IPUStrategy()

        with strategy.scope():

            optimizer = tf.keras.optimizers.SGD()

            input_layer = tf.keras.Input(shape=(1,))
            kernel_initializer = tf.keras.initializers.Constant(weight_value)
            x = tf.keras.layers.Dense(1, use_bias=False, kernel_initializer=kernel_initializer)(input_layer)
            model = tf.keras.Model(input_layer, x)

            model.build(input_shape=((1, 1)))

        @tf.function
        def ipu_fn():
            gradient = tf.constant([[gradient_value]], dtype=tf.float16)
            for _ in range(num_iterations):
                optimizer.apply_gradients(zip([gradient], model.trainable_variables))

        cfg = ipu.config.IPUConfig()
        cfg.auto_select_ipus = 1
        cfg.floating_point_behaviour.esr = stochastic_rounding
        cfg.device_connection.enable_remote_buffers = True
        cfg.device_connection.type = ipu.utils.DeviceConnectionType.ON_DEMAND
        cfg.configure_ipu_system()
        ipu.utils.reset_ipu_seed(42)

        strategy.run(ipu_fn)

        return model.get_weights()[0][0][0], weight_value

    def test_stochastic_rounding_enabled(self):

        weight_value_after_prog, weight_value_before_prog = self.run_ipu_prog(stochastic_rounding=True)

        self.assertNotEqual(weight_value_after_prog, weight_value_before_prog)

    def test_stochastic_rounding_disabled(self):

        weight_value_after_prog, weight_value_before_prog = self.run_ipu_prog(stochastic_rounding=False)

        self.assertEqual(weight_value_after_prog, weight_value_before_prog)
