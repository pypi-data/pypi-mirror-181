from milligrad.backend import *

class DenseNN(Module):

    def __init__(self, nin, nouts, activations):
        
        assert isinstance(nin, int), "nin must be int"
        assert isinstance(nouts, (tuple, list)), "nouts must be tuple or list"
        assert isinstance(activations, (tuple, list)), "activations must be tuple or list"
        assert len(nouts) == len(activations), f"layers and activations must have the same size. Size of layers is {len(nouts)} whilst size of activations is {len(activations)}"
        
        sz = (nin, ) + nouts if isinstance(nouts, tuple) else sz
        sz = [nin] + nouts if isinstance(nouts, list) else sz
                
        self.layers = [Layer(sz[i], sz[i+1], activations[i]) for i in range(len(nouts))]

    def __call__(self, x):
        for layer in self.layers:
            x = layer(x)
        return x

    def parameters(self):
        return [p for layer in self.layers for p in layer.parameters()]
    
    def Predict(self, input):
        
        assert isinstance(input, list) and isinstance(input[0], (int, float)), "inputs must be a 1-dimensional list of ints or floats"
        assert len(self.layers[0].neurons[0].w) == len(input), f"inputs lenght must match first 0-th layer size. 0-th layer has dimension {len(self.layers[0].neurons[0].w)} whilst inputs has size {len(input)}"
        
        return self(input)
    
    def Train(self, inputs, predictions, loss, epochs_number, batch_size, learning_rate, decay_rate = 0, L2_regularization = 0):
        
        def sum_parameters(parameters):
            sum = 0
            for p in parameters:
                sum += p.data**2 if p.label == 'weight' else 0
            return sum
        
        def learning_rate_decay(learning_rate, decay_rate, epoch):
            learning_rate=(1/(1+decay_rate*epoch))*learning_rate
            return learning_rate
        
        def update_parameters(self, learning_rate, batch_size, current_example, example_set_size):
            current_example += 1
            if (current_example % batch_size == 0) or (current_example==example_set_size):
                if (current_example==example_set_size) and (current_example % batch_size != 0):
                    batch_size = example_set_size % batch_size
                for parameter in self.parameters():
                    parameter.data -= (learning_rate/batch_size) * parameter.grad
        
        assert isinstance(inputs, list) and isinstance(inputs[0], list) and isinstance(inputs[0][0], (int, float)), "inputs must be 2-dimensional list of ints or floats"
        if self.layers[-1].neurons[0].nonlin == 'sigmoid':
            assert isinstance(predictions, list) and isinstance(predictions[0], (int, float)), "predictions must be 1-dimensional layer"
        if self.layers[-1].neurons[0].nonlin == 'softmax':
            assert isinstance(predictions, list) and isinstance(predictions[0], list) and isinstance(predictions[0][0], (int, float)), "predictions must be 2-dimensional layer"
            
        loss = loss.upper()
        
        assert loss == 'MSE' or loss == 'BCE' or loss == 'CCE' or loss == '', "loss function is not valid"
        
        #assign to loss_func the selected loss function
        if loss == 'MSE':
            loss_func = lambda n, x : n.MeanSquaredError(x)
        elif loss == 'BCE':
            loss_func = lambda n, x : n.BinaryCrossEntropy(x)
        elif loss == 'CCE':
            loss_func = lambda n, x : CategoricalCrossEntropy(n, x)
        else:
            loss_func = lambda x, y : x
        
        print("Training neural network...")
        print("Epoch", end=' ')
        for epoch in range(epochs_number):
            print(f"#{epoch+1}, ", end='')
            for example in range(len(inputs)):
                out = self(inputs[example]) #forward prop
                out = loss_func(out, predictions[example]) #computing loss
                out.data += L2_regularization * sum_parameters(self.parameters()) #L2 regularization
                out.backward() #backprop
                learning_rate = learning_rate_decay(learning_rate, decay_rate, epoch) #learning rate decay
                update_parameters(self, learning_rate, batch_size, example, len(inputs)) #wights and bias update
                self.zero_grad() #gradients must be set to 0 before next iteration
        print("\nNeural network successfully trained.")
        print(f"Last cost is {out.data}")
        return self

    def __repr__(self):
        return f"NeuralNetwork of [{', '.join(str(layer) for layer in self.layers)}]"