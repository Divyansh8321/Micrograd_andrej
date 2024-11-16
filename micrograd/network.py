from engine import Value
import numpy as np
import pandas as pd

class Module:
    def zero_grad(self):
        for p in self.parameters():
            p.grad = 0

    # Removing parameters here will cause you to not be able to call module.parameters() in a polymorphic way and will make the code less robust

    def parameters(self):
        parameters  = []

# As of now giving only relu and tanh as the non-linearity options

class Neuron (Module):
    def __init__(self , nin , _activation  = 'linear'):

        self.w = [Value(np.random.uniform(-1,1)) for _ in range(nin)]
        self.b = Value(np.random.uniform(-1,1))
        self._activation = _activation
    
    def __call__(self , x):
        out = sum((wi * xi for wi , xi in zip(self.w , x)) , self.b)
        if (self._activation == 'linear'):
            return out
        else :
            if (self._activation == 'relu'):
                out = out.relu()
            if (self._activation == 'tanh'):
                out = out.tanh()

        return out

    def parameters(self):
        parameters = [self.b] + self.w
        return parameters
    
    def __repr__(self):
        return f'Neuron with activation function as {self._activation}'
    
class Layer (Module):

    def __init__(self , nin , nout , _activation):
        self.neurons = [Neuron(nin , _activation) for _ in range(nout)]
        self.layer_size = nout
        self._activation = _activation
    
    def __call__(self , x):
        out = []
        for neuron in self.neurons:
            out.append(neuron(x))
        return out
    
    def parameters(self):
        parameters = []
        for neuron in self.neurons :
            parameters.extend(neuron.parameters())
        return parameters
        
    def __repr__ (self):
        return f' This is layer consisting of {self.layer_size} neurons with the activation function {self._activation}'

class MLP (Module):

    def __init__(self , nin , nouts , _activations):
        self.n_layers = len(nouts)
        sz = [nin] + nouts
        self._activations = _activations
        self.layers = [Layer(sz[i] , sz[i+1] , self._activations[i]) for i in range(self.n_layers)]
    
    def __call__(self , x):
        
        for layer in self.layers:
            x = layer(x)
        return x[0] if len(x) == 1 else x
    
    def parameters(self):
        parameters = []
        for layer in self.layers:
            parameters.extend(layer.parameters())

        return parameters 
    
    def __repr__(self):
        return f'This is a MLP of {self.n_layers} layers'



 