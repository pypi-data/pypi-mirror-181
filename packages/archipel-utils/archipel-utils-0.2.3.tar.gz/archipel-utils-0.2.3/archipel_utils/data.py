"""Copyright Alpine Intuition Sàrl team.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import base64
import io

import numpy as np

try:
    import cv2

    OPENCV_AVAILABLE = True
except ModuleNotFoundError:
    OPENCV_AVAILABLE = False


def serialize_array(array: np.ndarray) -> bytes:
    """Serialize a numpy array into bytes."""

    if (
        array.dtype not in [np.uint16, np.float32]
        and len(array.shape) == 3
        and OPENCV_AVAILABLE
    ):
        # basic image
        success, encoded_array = cv2.imencode(".png", array)
        if not success:
            raise ValueError("Fail to encode array")
        return base64.b64encode(encoded_array)
    else:
        buffer = io.BytesIO()
        np.save(buffer, array)
        return buffer.getvalue()


def deserialize_array(serialized_array: bytes) -> np.ndarray:
    """Serialize a bytes variable into numpy array."""
    try:
        # serialized data from python
        return np.load(io.BytesIO(serialized_array))
    except ValueError:
        # serialized data from other sources
        if not OPENCV_AVAILABLE:
            raise ModuleNotFoundError("opencv-python is not available")
        deserialized_array = base64.b64decode(serialized_array)
        array = np.frombuffer(deserialized_array, dtype=np.uint8)
        data = cv2.imdecode(array, cv2.IMREAD_UNCHANGED)
        if len(data.shape) == 2:
            # to be sure to keep the empty dim for color
            data = np.expand_dims(data, axis=2)
        return data
