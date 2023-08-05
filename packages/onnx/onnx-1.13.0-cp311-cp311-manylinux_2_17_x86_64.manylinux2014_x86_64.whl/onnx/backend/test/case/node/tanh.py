# SPDX-License-Identifier: Apache-2.0

import numpy as np

import onnx

from ..base import Base
from . import expect


class Tanh(Base):
    @staticmethod
    def export() -> None:
        node = onnx.helper.make_node(
            "Tanh",
            inputs=["x"],
            outputs=["y"],
        )

        x = np.array([-1, 0, 1]).astype(np.float32)
        y = np.tanh(x)  # expected output [-0.76159418, 0., 0.76159418]
        expect(node, inputs=[x], outputs=[y], name="test_tanh_example")

        x = np.random.randn(3, 4, 5).astype(np.float32)
        y = np.tanh(x)
        expect(node, inputs=[x], outputs=[y], name="test_tanh")
