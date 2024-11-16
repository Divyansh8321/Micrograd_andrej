# Mock for creating the micrograd in python by myself:
import numpy as np

# Creating a class called Value which sort of acts as the base for our Micrograd (similar to int or float or double)
class Value():

    def __init__(self , data , _children = () , _operation = ''):
        self.data = data
        self._prev = set(_children)
        self._operation = _operation
        self.grad = 0 
        self._backward = lambda: None

    def __repr__(self):
        return f'The Value is {self.data} and the grad is {self.grad}'

    def __add__(self , other):
        other = other if isinstance(other , Value) else Value(other)
        out = Value(self.data + other.data , (self , other) , '+')

        def _backward():
            self.grad += out.grad
            other.grad += out.grad

        # This is basically creating the function for performing backprop on out and diverting the gradient to the children of this addition
        # We are simply creating a method and then assigning that method to out
        # So that when out.backward() is called eventually on the loss fucntion each operation's (+ , * , -) output knows how to send back the gradients

        out._backward = _backward
        return out 
    
    def __mul__(self , other):
        other = other if isinstance(other , Value) else Value(other)
        out = Value(self.data * other.data , (self , other) , '*')

        def _backward():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad

        out._backward = _backward
        return out

    
    def __pow__(self , other):
        assert (isinstance(other , (float , int))) , "The input must be float or int for now"
        # Do not add other to the children here since it is only a float or a int which will throw an error since you wont be able to call backward there 
        out = Value(self.data ** (other) , (self ,) , '^')

        def _backward():
            self.grad += other * (self.data ** (other-1)) * out.grad
        out._backward = _backward
        return out

    def relu(self):
        out = Value(max(0 , self.data) , (self,) , 'relu')

        def _backward():
            self.grad += out.grad if (self.data > 0) else 0
        
        out._backward = _backward
        return out


    def tanh(self):
        t = np.tanh(self.data)
        out = Value(t , (self,) , 'tanh')

        def _backward():
            self.grad += (1-t**2)*out.grad
        
        out._backward = _backward
        return out

    def exp(self):
        t = np.exp(self.data)
        out = Value(t , (self , ) , 'e^x')

        def _backward(): 
            self.grad += t*out.grad
        
        out._backward = _backward
        return out
    
    def __rmul__ (self , other):
        out = self * other
        return out
    

    # Will not need to wrap in a Value object if we leverage the multiplication template but then you will need to use self instead of self.data here
    # Same as above for others leveraging the previous methods
    
    # Here would have had to describe the backprop gradient flow myself but can leverage the already defined multiplication and power
    # def __truediv__(self , other):
    #     other = other if isinstance(other , Value) else Value(other)
    #     out =  self.data * (1/other.data)
    #     return Value(out)

    def __truediv__(self , other):
        out = self * (other**(-1))
        return out
    
    def __sub__(self , other):
        out = self + (other * -1)
        return out

    def __neg__(self):
        out = self * -1
        return out
    
    def backward(self):
        # Doing a topological sort to find the right order of operations
        topo = []
        visited = set()
        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build_topo(child)
                topo.append(v)
        build_topo(self)

        self.grad = 1

        for node in reversed(topo):
            node._backward()

