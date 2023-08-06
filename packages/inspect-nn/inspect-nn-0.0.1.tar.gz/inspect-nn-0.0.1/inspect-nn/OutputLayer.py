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
from .BaseLayer import BaseLayer

class OutputLayer(BaseLayer):
    def __init__(self, activation = "relu", name = "layer"):
        BaseLayer.__init__(self, activation, name = name)

    def __deepcopy__(self, memo = None):
        pass

    def load_weights(self, **kwargs):
        self.input_shape = kwargs["input_shape"]

        self.output_shape = self.input_shape
        
        return self.output_shape
    
    def forward_pass(self, **kwargs):
        inputv = kwargs["inputv"]
        if self.activation is not None:
            return BaseLayer.activations[self.activation](inputv)
        return inputv
