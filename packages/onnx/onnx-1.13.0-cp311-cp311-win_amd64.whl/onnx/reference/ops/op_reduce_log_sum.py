# SPDX-License-Identifier: Apache-2.0
# pylint: disable=W0221

import numpy as np

from onnx.defs import onnx_opset_version

from ._op import OpRunReduceNumpy


class ReduceLogSum_1(OpRunReduceNumpy):
    def _run(self, data, axes=None, keepdims=True):  # type: ignore
        tax = tuple(axes) if axes else None
        res = np.sum(data, axis=tax, keepdims=keepdims)
        if len(res.shape) > 0:
            return (np.log(res, out=res),)
        return (np.log(res),)


class ReduceLogSum_11(ReduceLogSum_1):
    pass


class ReduceLogSum_13(ReduceLogSum_1):
    pass


class ReduceLogSum_18(OpRunReduceNumpy):
    def run(self, data, axes=None, keepdims=None, noop_with_empty_axes=None):  # type: ignore
        keepdims = keepdims or self.keepdims  # type: ignore
        noop_with_empty_axes = noop_with_empty_axes or self.noop_with_empty_axes  # type: ignore
        return self._run(data, axes, keepdims, noop_with_empty_axes)

    def _run(self, data, axes, keepdims=1, noop_with_empty_axes=0):  # type: ignore
        if self.is_axes_empty(axes) and noop_with_empty_axes:  # type: ignore
            return (data,)

        axes = self.handle_axes(axes)
        keepdims = keepdims != 0  # type: ignore

        res = np.sum(data, axis=axes, keepdims=keepdims)
        if len(res.shape) > 0:
            return (np.log(res, out=res),)
        return (np.log(res),)


if onnx_opset_version() >= 18:
    ReduceLogSum = ReduceLogSum_18
elif onnx_opset_version() >= 13:
    ReduceLogSum = ReduceLogSum_13  # type: ignore
elif onnx_opset_version() >= 11:
    ReduceLogSum = ReduceLogSum_11  # type: ignore
else:
    ReduceLogSum = ReduceLogSum_1  # type: ignore
