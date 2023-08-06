"""
Copyright 2022  Salvatore Barone <salvatore.barone@unina.it>
                Filippo Ferrandino <fi.ferrandino@studenti.unina.it>

This is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free
Software Foundation; either version 3 of the License, or any later version.

This is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
more details.

You should have received a copy of the GNU General Public License along with
RMEncoder; if not, write to the Free Software Foundation, Inc., 51 Franklin
Street, Fifth Floor, Boston, MA 02110-1301, USA.
"""
import numpy as np
from scipy.special import softmax
from functools import partial

class BaseLayer:
    relu = partial(np.maximum, 0)
    max3d = partial(np.max, axis=(0, 1))
    avg3d = partial(np.mean, axis=(0, 1))
    activations = {"relu" : relu, "softmax" : softmax}
    poolings3d = {"max" : max3d, "avg" : avg3d}
    default_multiplier = np.multiply

    def __init__(self, 
            activation = "relu", quant_nbits = 8, multiplier = default_multiplier, name = "layer", 
            enable_gpu = False, gpu_input_memory = None, gpu_output_memory = False, blockdim = (1, 1)):
        self.activation = activation
        self.quant_nbits = quant_nbits
        self.multiplier = multiplier
        self.name = name
        self.weights = None
        self.biases = None
        self.enable_multiprocess = False
        self.enable_gpu = enable_gpu
        self.results = None
        self.use_gpu = False
        self.gpu_output_memory = gpu_output_memory #se è vero non devo passare i dati da results ad outptv
        self.gpu_input_memory = gpu_input_memory  #se è diverso da null non devo spostare i dati in ingresso su gpu (dovrei avere gia l' area di memoria)
        self.blockdim = blockdim # TODO: va calcolato in base alla GPU
        
    def __deepcopy__(self, memo = None):
        return BaseLayer(activation = self.activation, quant_nbits = self.quant_nbits, multiplier = self.multiplier, name = self.name, enablegpu = self.enable_gpu)

    def load_weights(self, **kwargs):
        self.enable_gpu = kwargs["enable_gpu"]
        
        self.weights, self.biases = kwargs["weights"], kwargs["biases"]
            
    def forward_pass(self, **kwargs):
        pass
