from math import tanh, exp, log
from graphviz import Digraph

class Value:
    """ stores a single scalar value and its gradient """

    def __init__(self, data, _children=(), _op='', label=''):
        self.data = data
        self.grad = 0
        self.label = label
        # internal variables used for autograd graph construction
        self._backward = lambda: None
        self._prev = set(_children)
        self._op = _op # the op that produced this node, for graphviz / debugging / etc

    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other), '+')
        
        def _backward():
            self.grad += out.grad
            other.grad += out.grad
            
        out._backward = _backward
        return out
    
    def multisum(self, addends):
        x = self.data
        for i in range(len(addends)):
            x += addends[i].data
        out = Value(x, (self, ) + addends, '+')
        
        def _backward():
            self.grad += out.grad
            for i in range(len(addends)):
                addends[i].grad += out.grad
        out._backward=_backward
        
        return out
    
    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other), '*')
        
        def _backward():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
            
        out._backward = _backward
        return out

    def __pow__(self, other):
        assert isinstance(other, (int, float)), "only supporting int/float powers for now"
        out = Value(self.data**other, (self,), f'**{other}')
        
        def _backward():
            self.grad += (other * self.data**(other-1)) * out.grad
            
        out._backward = _backward
        return out

    def exp(self):
        x = exp(self.data)
        out = Value(x, (self, ), 'exp')
        
        def _backward():
            self.grad = x * out.grad
        
        out._backward = _backward
        return out

    def relu(self):
        out = Value(0 if self.data < 0 else self.data, (self,), 'ReLU')
        
        def _backward():
            self.grad += (out.data > 0) * out.grad
            
        out._backward = _backward
        return out
    
    def tanh(self):
        x = tanh(self.data)
        out = Value(x, (self, ), 'tanh')
        
        def _backward():
            self.grad += (1-x**2) * out.grad
            
        out._backward = _backward
        return out
    
    def sigmoid(self):
        x = 1/(1+(exp(-self.data)))
        out = Value(x, (self, ), 'sigmoid')
        
        def _backward():
            self.grad += (x-x**2) * out.grad
            
        out._backward = _backward
        return out  
    
    def MeanSquaredError(self, pred):
        x = 0.5*(self.data - pred)**2
        out = Value(x, (self, ), 'MSE')
        
        def _backward():
            self.grad += (self.data-pred) * out.grad
        
        out._backward = _backward
        return out
    
    def BinaryCrossEntropy(self, pred):
        y_hat = self.data
    
        x = -pred * log(y_hat) - (1-pred) * log(1-y_hat)
        out = Value(x, (self, ), 'BCE')
        
        def _backward():
            self.grad += (-(pred/y_hat) + (1-pred)/(1-y_hat)) * out.grad
        
        out._backward = _backward
        return out
    
    def CategoricalCrossEntropy(self, others, pred):
        x = pred[0] * log(self.data)
        for i in range(len(others)):
            x += pred[i+1] * log(others[i].data)
        out = Value(x, (self,) + others, 'CCE')
        
        def _backward():
            self.grad += pred[0] * self.data * out.grad
            for i in range(len(others)):
                others[i].grad += pred[i] * others[i].data * out.grad
        
        out._backward = _backward
        return out

    def backward(self):
        # topological order all of the children in the graph
        topo = []
        visited = set()
        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build_topo(child)
                topo.append(v)
        build_topo(self)
        # go one variable at a time and apply the chain rule to get its gradient
        
        self.grad = 1
        for v in reversed(topo):
            v._backward()

    def __neg__(self): # -self
        return self * -1

    def __radd__(self, other): # other + self
        return self + other

    def __sub__(self, other): # self - other
        return self + (-other)

    def __rsub__(self, other): # other - self
        return other + (-self)

    def __rmul__(self, other): # other * self
        return self * other

    def __truediv__(self, other): # self / other
        return self * other**-1

    def __rtruediv__(self, other): # other / self
        return other * self**-1

    def __repr__(self):
        return f"Value(data={self.data}, grad={self.grad})"
    
    def graph(self):
        def trace(root):
            nodes, edges = set(), set()
            def build(v):
                if v not in nodes:
                    nodes.add(v)
                    for child in v._prev:
                        edges.add((child, v))
                        build(child)
            build(root)
            return nodes, edges
        
        nodes, edges = trace(self)
        dot = Digraph(format='svg', graph_attr={'rankdir': 'LR'}) #, node_attr={'rankdir': 'TB'})
        
        for n in nodes:
            if n.label == "weight" or n.label == "bias":
                dot.node(name=str(id(n)), label = "{ %s | data %.4f | grad %.4f }" % (n.label, n.data, n.grad), shape='record')
            else:
                if len(n._prev) == 0:
                    dot.node(name=str(id(n)), label = "{ %s | data %.4f }" % ('input', n.data), shape='record')
                else:
                    dot.node(name=str(id(n)), label = "{ data %.4f | grad %.4f }" % (n.data, n.grad), shape='record')
            if n._op:
                dot.node(name=str(id(n)) + n._op, label=n._op)
                dot.edge(str(id(n)) + n._op, str(id(n)))
        
        for n1, n2 in edges:
            dot.edge(str(id(n1)), str(id(n2)) + n2._op)
        
        dot.view()

def softmax(neurons):
    sum = 0
    for n in neurons:
        sum = sum + n.exp()
    
    out = []
    for n in neurons:
        n = n.exp()/sum
        out.append(n)        
    return out 

def CategoricalCrossEntropy(neurons, pred):
        x = 0
        for i in range(len(neurons)):
            x += - pred[i] * log(neurons[i].data)
        out = Value(x, neurons, 'CCE')
        
        def _backward():
            for i in range(len(neurons)):
                neurons[i].grad += (neurons[i].data - pred[i]) * out.grad
        
        out._backward = _backward
        return out