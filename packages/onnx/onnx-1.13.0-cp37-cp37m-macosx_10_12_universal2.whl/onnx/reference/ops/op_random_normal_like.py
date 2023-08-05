# SPDX-License-Identifier: Apache-2.0
# pylint: disable=R0913,W0221

from onnx.helper import np_dtype_to_tensor_dtype

from ._op_common_random import _CommonRandom


class RandomNormalLike(_CommonRandom):
    def _run(self, x, dtype=None, mean=None, scale=None, seed=None):  # type: ignore
        if dtype is None:
            dtype = np_dtype_to_tensor_dtype(x.dtype)
        dtype = self._dtype(x, dtype=dtype)
        state = self._get_state(seed)
        res = state.randn(*x.shape).astype(dtype)
        res *= scale  # type: ignore
        res += mean  # type: ignore
        return (res.astype(dtype),)
