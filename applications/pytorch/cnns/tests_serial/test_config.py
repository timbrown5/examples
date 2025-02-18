# Copyright (c) 2021 Graphcore Ltd. All rights reserved.
import gc
import pytest
import import_helper
from utils import run_script


@pytest.mark.ipus(0)
@pytest.mark.parametrize("config", ["efficientnet-b0-g16-gn-16ipu-mk2", "efficientnet-b4-g16-gn-16ipu-mk2", "resnet50_mk2", "resnet50_mk2_pod64",
                                    "mobilenet-v3-large-pod16", "mobilenet-v3-small-pod4"])
def test_train_config_compile(config):
    gc.collect()
    out = run_script("train/train.py", f"--data generated --config {config} --compile-only --checkpoint-path temp_folder")
    assert not("ERROR" in out)


@pytest.mark.ipus(1)
@pytest.mark.parametrize("config", ["resnet50-mk2", "efficientnet-b0-mk2", "efficientnet-b4-mk2", "efficientnet-b0-g16-gn-mk2", "efficientnet-b4-g16-gn-mk2",
                                    "mobilenet-v3-small-mk2", "mobilenet-v3-large-mk2"])
def test_inference_config(config):
    gc.collect()
    out = run_script("inference/run_benchmark.py", f"--data generated --config {config} --dataloader-worker 2 --iterations 5 --device-iteration 1")
    assert not("ERROR" in out)
