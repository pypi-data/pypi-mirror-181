from milligrad.engine import Value
from milligrad.engine import CategoricalCrossEntropy, softmax
import random

class Module:

    def zero_grad(self):
        for p in self.parameters():
            p.grad = 0

    def parameters(self):
        return []

class Neuron(Module):

    def __init__(self, nin, nonlin):
        self.w = [Value(random.gauss(0, 1/nin), label = 'weight') for _ in range(nin)] #Xavier initialization
        self.b = Value(0, label = 'bias')
        self.nonlin = nonlin

    def __call__(self, x):
        act=()
        for wi, xi in zip(self.w, x):
            act += (wi*xi, )
        act += (self.b, )
        act = act[0].multisum(act[1:])
        
        self.nonlin = self.nonlin.lower()
        
        assert self.nonlin in ('', 'linear', 'sigmoid', 'relu', 'tanh', 'softmax'), f"{self.nonlin} is not a valid activation function. Valid activation functions are: linear, relu, sigmoid, tanh, softmax"
        
        # act = act if self.nonlin == ('linear' or '') else act
        act = act.relu() if self.nonlin == 'relu' else act
        act = act.sigmoid() if self.nonlin == 'sigmoid' else act
        act = act.tanh() if self.nonlin == 'tanh' else act

        return act
        
    def parameters(self):
        return self.w + [self.b]

    def __repr__(self):
        nonlin = self.nonlin.capitalize() #just for nicer visualization
        nonlin = 'ReLU' if self.nonlin.lower() == 'relu' else nonlin #just for nicer visualization
            
        return f"{nonlin}Neuron({len(self.w)})"

class Layer(Module):

    def __init__(self, nin, nout, activation):
        self.neurons = [Neuron(nin, activation) for _ in range(nout)]

    def __call__(self, x):
        out = [n(x) for n in self.neurons]
        if self.neurons[0].nonlin == 'softmax':
            out = softmax(out)
        return out[0] if len(out) == 1 else out

    def parameters(self):
        return [p for n in self.neurons for p in n.parameters()]

    def __repr__(self):
        return f"Layer of [{', '.join(str(n) for n in self.neurons)}]"
    
