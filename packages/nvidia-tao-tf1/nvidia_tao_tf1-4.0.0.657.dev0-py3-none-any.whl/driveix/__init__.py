# Copyright (c) 2018, NVIDIA CORPORATION. All rights reserved.

"""DriveIX module."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Apply keras mmonkey patch
import third_party.keras.mixed_precision as MP
import third_party.keras.tensorflow_backend as TFB

MP.patch()
TFB.patch()
