from engine import Value
from network import Neuron , Layer , MLP
import numpy as np

np.random.seed(42)
# Let's test by making a simple Neuron and then calling backprop on it to train it

single_neuron = Neuron(1 , 'linear')
x = [[Value(1)] , [Value(2)] , [Value(3)] , [Value(4)] , [Value(5)]]
y = [Value(1) , Value(2) , Value(3) , Value(4) , Value(5)]

for epoch in range (100):
    y_pred = []
    for inp in x:
        y_pred.append(single_neuron(inp))

    # Sum returns int by default unless you mention the initial data type like i have here with using a 0 and similarly in the Neuron code using self.b
    loss = sum(((y_pred[i] - y[i])**2 for i in range (len(y))) , Value(0))
    loss.backward()

    print(f"Epoch {epoch}, Loss: {loss.data}")
    for p in single_neuron.parameters():
        p.data -= 0.01 * p.grad
    single_neuron.zero_grad()


    
