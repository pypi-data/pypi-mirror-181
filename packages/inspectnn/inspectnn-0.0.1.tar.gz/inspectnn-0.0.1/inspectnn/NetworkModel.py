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

import numpy as np, json, copy, tensorflow as tf, time
from distutils.dir_util import mkpath
from .ConvLayer import ConvLayer
from .DenseLayer import DenseLayer
from .PoolingLayer import PoolingLayer
from .FlattenLayer import FlattenLayer
from .OutputLayer import OutputLayer
from .utils import grouped, flatten


class NetworkModel:
    def __init__(self, learned_parameters, layers,input_shape):
        self.learned_parameters = learned_parameters
        self.layers = layers
        self.outputs = []
        self.input_shape=input_shape
        
        self.total_time = 0
        self.elapsed_time = np.zeros(len(layers))
        gpu_input_memory=None
        
        lp = 0
        last_layer=None
        for layer in self.layers:
            if isinstance(layer, (ConvLayer, DenseLayer)):
                output_shape =layer.load_weights(input_shape = input_shape, weights = self.learned_parameters[lp], biases = self.learned_parameters[lp + 1],enable_gpu=tf.test.is_gpu_available(),gpu_input_memory=gpu_input_memory)
                lp += 2
           
            elif isinstance(layer, (PoolingLayer, FlattenLayer, OutputLayer)):
                output_shape =layer.load_weights(input_shape = input_shape,enable_gpu=tf.test.is_gpu_available(),gpu_input_memory=gpu_input_memory)
                
            else:
                print(f"Layer {type(layer)} not supported yet")
            
            gpu_input_memory=layer.results
            if layer.use_gpu  and   last_layer != None and last_layer.use_gpu:
                last_layer.gpu_output_memory = True
            else:
                print(f"Layer {type(layer)} no gpu")


            input_shape = output_shape
            last_layer = layer
        

    def __deepcopy__(self, memo = None):
        return NetworkModel(self.learned_parameters, copy.deepcopy(self.layers),self.input_shape)

    def export_learned_parameters(self, outdir):
        mkpath(outdir)
        learned_weights = []
        learned_biases  = []
        for i, param in enumerate(grouped(self.learned_parameters, 2)):
            weights = list(flatten(param[0].astype(int).tolist()))
            biases = list(flatten(param[1].astype(int).tolist()))
            with open(f"{outdir}/layer_weights_{i}.json", 'w') as outfile:
                outfile.write(json.dumps(weights))
            with open(f"{outdir}/layer_biases_{i}.json", 'w') as outfile:
                outfile.write(json.dumps(biases))
            learned_weights.append(weights)
            learned_biases.append(biases)
        learned_weights = list(flatten(learned_weights))
        learned_biases = list(flatten(learned_biases))
        with open(f"{outdir}/full_net_weights.json", 'w') as outfile:
            outfile.write(json.dumps(learned_weights)) 
        with open(f"{outdir}/full_net_biases.json", 'w') as outfile:
            outfile.write(json.dumps(learned_biases))

    def predict(self, test_image):
        self.outputs = [test_image]
        for idx, layer in enumerate(self.layers):
            st = time.time()
            if isinstance(layer, (ConvLayer, DenseLayer,PoolingLayer, FlattenLayer, OutputLayer)):
                self.outputs.append(layer.forward_pass(inputv = self.outputs[-1]))
            else:
                print(f"Layer {type(layer)} not supported yet")
            #input_layer.append(outputs)
            et = time.time()
            self.elapsed_time[idx] += et - st
            self.total_time += et - st
        return self.outputs[-1] / np.max(self.outputs[-1])
        
    def print_time_statics(self):
        print(f"Total Time = {self.total_time}")
        for idx, layer in enumerate(self.layers):
            print(f"Layer {type(layer)} # time {self.elapsed_time[idx]}s # ( {self.elapsed_time[idx]/self.total_time*100}% ) #GPU {layer.use_gpu} - GPU_OUT {layer.gpu_output_memory}")
            
    #@staticmethod
    def mimt_do_inference(self, labels, images):
        assert isinstance(labels, (list, tuple))
        assert isinstance(images, (list, tuple))
        assert len(labels) == len(images)
        return [np.array_equal(self.predict(i)[0], l) for l, i in zip(labels, images)]

    #@staticmethod
    def evaluate_accuracy(self, labels, images):
        assert isinstance(labels, (list, tuple))
        assert isinstance(images, (list, tuple))
        assert len(labels) == len(images)
        outputv = self.mimt_do_inference(list(labels),list(images))
        return np.sum(flatten(outputv)) / len(labels) * 100