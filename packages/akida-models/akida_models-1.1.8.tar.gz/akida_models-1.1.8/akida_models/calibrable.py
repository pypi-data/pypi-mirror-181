#!/usr/bin/env python
# ******************************************************************************
# Copyright 2022 Brainchip Holdings Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ******************************************************************************
"""Tools for calibration"""

import tensorflow as tf
from quantizeml.layers import Calibrable, CalibrableVariable


def calibration_required(model):
    """Checks if a model must be calibrated at training time.

    Args:
        model (keras.Model): the model to check

    Returns:
        bool: True if a calibration is required before a train or tune action.
    """
    # model is not calibrable
    cal_layers = [ly for ly in model.layers if isinstance(ly, Calibrable)]
    if len(cal_layers) == 0:
        return False

    for layer in cal_layers:
        for name in layer.calibrables:
            calibrable = getattr(layer, name)
            # if the model has never been calibrated, all max_value of the Calibrable objects
            # will be set to 1, and all CalibrableVariables should be equal to zero.
            default_value = 0 if isinstance(calibrable, CalibrableVariable) else 1
            if tf.reduce_any(calibrable.variables[0] != default_value):
                return False

    # all calibrable objects and variables are unset
    return True
