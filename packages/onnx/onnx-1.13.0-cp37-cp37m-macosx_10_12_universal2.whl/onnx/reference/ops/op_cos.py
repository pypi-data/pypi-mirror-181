# SPDX-License-Identifier: Apache-2.0
# pylint: disable=W0221

import numpy as np

from ._op import OpRunUnaryNum


class Cos(OpRunUnaryNum):
    def _run(self, x):  # type: ignore
        return (np.cos(x),)
