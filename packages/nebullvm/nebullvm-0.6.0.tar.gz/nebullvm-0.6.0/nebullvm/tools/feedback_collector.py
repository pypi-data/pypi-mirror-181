import json
import os
import platform
import select
import sys
import uuid
from pathlib import Path
from typing import Any, Optional

import psutil
import requests
from cpuinfo import cpuinfo


from nebullvm.config import VERSION
from nebullvm.optional_modules.torch import Module
from nebullvm.optional_modules.utils import (
    torch_is_available,
    tensorflow_is_available,
)
from nebullvm.tools.base import (
    DeepLearningFramework,
    Device,
    ModelCompiler,
    QuantizationType,
)
from nebullvm.tools.pytorch import torch_get_device_name
from nebullvm.tools.tf import tensorflow_get_gpu_name

NEBULLVM_METADATA_PATH = Path.home() / ".nebullvm/collect.json"


def _input_with_timeout(message: str, timeout: int):
    print(message)
    i, o, e = select.select([sys.stdin], [], [], timeout)
    if i:
        input_str = sys.stdin.readline().strip()
    else:
        raise TimeoutError()
    return input_str


def _read_model_size(model: Any):
    if isinstance(model, str) or isinstance(model, Path):
        size = os.stat(str(model)).st_size
    elif isinstance(model, Module):
        size = sum(
            param.nelement() * param.element_size()
            for param in model.parameters()
        )
    else:
        # we assume it is a tf_model
        size = model.count_params() * 4  # assuming full precision 32 bit
    return f"{round(size * 1e-6, 2)} MB"


def _get_gpu_name():
    if torch_is_available():
        name = torch_get_device_name()
    elif tensorflow_is_available():
        name = tensorflow_get_gpu_name()
    else:
        name = "Unknown GPU"

    return name


class FeedbackCollector:
    def __init__(self):
        if NEBULLVM_METADATA_PATH.exists():
            with open(NEBULLVM_METADATA_PATH, "r") as f:
                nebullvm_metadata = json.load(f)
        else:
            nebullvm_metadata = self._ask_permissions()
            NEBULLVM_METADATA_PATH.parent.mkdir(exist_ok=True)
            with open(NEBULLVM_METADATA_PATH, "w") as f:
                json.dump(nebullvm_metadata, f)
        self._is_active = nebullvm_metadata["allow_feedback_collection"]
        self._model_info = None
        self._model_id = None
        self._latency_dict = None
        self._hw_info = {
            "cpu": cpuinfo.get_cpu_info()["brand_raw"],
            "operative_system": platform.system(),
            "ram": f"{round(psutil.virtual_memory().total * 1e-9, 2)} GB",
        }

    @property
    def is_active(self):
        return self._is_active

    @staticmethod
    def _ask_permissions(timeout: int = 30):
        message = (
            "Would you like to contribute to nebullvm continuous improvement? "
            "Press enter to share the performance achieved with nebullvm and "
            '"No" to not contribute. You can find full details in the '
            '"Sharing feedback to improve nebullvm" section of the '
            'documentation. [enter/"No"] '
        )
        metadata = {}
        flag = True
        while flag:
            try:
                collect_feedback_bool = _input_with_timeout(message, timeout)
            except (TimeoutError, OSError):
                collect_feedback_bool = "no"
            if len(collect_feedback_bool) == 0:
                flag = False
                metadata["allow_feedback_collection"] = True
            elif collect_feedback_bool.lower().strip() == "no":
                flag = False
                metadata["allow_feedback_collection"] = False
            message = (
                'Press enter to give your consent or type "No" to deny '
                "consent."
            )
        return metadata

    @staticmethod
    def _generate_model_id(model_name: str):
        return f"{str(uuid.uuid4())}_{hash(model_name)}"

    def start_collection(
        self, model: Any, framework: DeepLearningFramework, device: Device
    ):
        if isinstance(model, str) or isinstance(model, Path):
            model_name = str(model)
        else:
            model_name = model.__class__.__name__

        if device is Device.GPU:
            self._hw_info["gpu"] = _get_gpu_name()
        self._model_id = self._generate_model_id(model_name)
        self._model_info = {
            "model_name": model_name,
            "model_size": _read_model_size(model),
            "framework": framework.value,
        }
        self._latency_dict = {}

    def store_compiler_result(
        self,
        compiler: ModelCompiler,
        q_type: Optional[QuantizationType],
        metric_drop_ths: Optional[float],
        latency: Optional[float],
        pipeline_name: DeepLearningFramework,
        compression: str = None,
    ):
        if self._model_id is None:
            return
        q_type_key = (
            f"{q_type.value}_{metric_drop_ths}"
            if q_type is not None and metric_drop_ths is not None
            else "noopt"
        )
        if compression is not None and len(compression) > 0:
            q_type_key = compression + "_" + q_type_key
        pipeline_name = (
            pipeline_name.value
            if pipeline_name is not DeepLearningFramework.NUMPY
            else "onnx"
        )
        key = pipeline_name + "_" + compiler.value
        compiler_dict = self._latency_dict.get(key, {})
        compiler_dict[q_type_key] = latency if latency else -1.0
        self._latency_dict[key] = compiler_dict

    def send_feedback(self, store_latencies, timeout: int = 30):
        if self._model_id is None:
            return {}
        request_body = {
            "model_id": self._model_id,
            "latency_dict": self._latency_dict,
            "hardware_setup": self._hw_info,
            "model_metadata": self._model_info,
            "nebullvm_version": VERSION,
        }

        if store_latencies:
            model_name = self._model_info["model_name"]
            with open(
                f"latencies_{model_name}_{self._model_id}.json",
                "w",
            ) as fp:
                json.dump(request_body, fp)

        if self.is_active:
            headers = {
                "accept": "application/json",
                "Content-Type": "application/json",
            }
            url = "https://nebuly.cloud/v1/store_nebullvm_results"
            response = requests.post(
                url,
                data=json.dumps(request_body),
                headers=headers,
                timeout=timeout,
            )
        else:
            response = None

        self._model_id = None
        self._latency_dict = None
        self._model_info = None
        return response


FEEDBACK_COLLECTOR = FeedbackCollector()
