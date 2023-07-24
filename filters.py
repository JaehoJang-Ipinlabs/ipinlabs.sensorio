import numpy as np
import copy

# Frequency Suppression Filters
class LowPass:
    def __init__(self, wn):
        self.wn = wn # Hz
        x = np.exp(-2*np.pi*wn)
        self.a0 = 1-x
        self.b1 = x
        self.y = None
    def __call__(self, x):
        self.y = np.zeros_like(x)
        self.y[0] = self.a0 * x[0]
        for i in range(1,len(x)):
            # self.y is y[n] (left) or y[n-1] (right), while x[i] = x[n]
            self.y[i] = self.b1 * self.y[i-1] + self.a0 * x[i]
        return self.y
    
class HighPass:
    def __init__(self, wn):
        self.wn = wn
        x = np.exp(-2*np.pi*wn)
        self.a0 = (1+x)/2
        self.a1 = -(1+x)/2
        self.b1 = x
        self.y = None
    def __call__(self, x):
        self.y = np.zeros_like(x)
        self.y[0] = self.a0 * x[0]
        for i in range(1,len(x)):
            self.y[i] = self.b1 * self.y[i-1] + self.a0 * x[i] + self.a1 * x[i-1]
        return self.y

# Numerical Integrations in Recursive Forms
class Integral:
    '''
    Base class for Recursive Numerical Integrations
    '''
    def __init__(self):
        '''
        Init for Integral class.
        '''
        self.kernel = np.zeros((2,1))
        self.buffer = [np.array([[0]])]
    def __call__(self, x, dt, delta):
        '''
        x : Data to integrate, with shape of (n_samples, n_features)
        dt : difference of timestamps. float or an array with shape of (n_samples - 1, n_features)
        delta : delta (width) of X.
        '''
        return None
    def __forward__(self, x):
        return self.kernel @ x
    
class IntegralRiemann(Integral):
    '''
    Recursive Numerical Integration using Riemann Sum
    '''
    def __init__(self):
        super().__init__()
        self.method_list = ['trapezoidal', 'midpoint', 'left', 'right', 'upper', 'lower']
    def __call__(self, x, dt, delta, method = 'trapezoidal'):
        '''
        method : 'trapezoidal', 'midpoint', 'left', 'right', 'upper', 'lower'
        '''
        self.buffer = [np.array([[0]])]
        try:
            method_case = self.method_list.index(method)
        except ValueError as e:
            print('Method should be one of {}. The given method is {}'.format(self.method_list, '\'' + method + '\'.'))
        except Exception as e:
            print(e)
            
        if method_case == 0:
            self.kernel = np.array([[1/2*dt,1/2*dt]])
        elif method_case == 1:
            pass
        elif method_case == 2:
            self.kernel = np.zeros((1,delta+1))
            self.kernel[0,0] = dt
        elif method_case == 3:
            self.kernel = np.zeros((1,delta+1))
            self.kernel[0,1] = dt
        elif method_case == 4:
            self.kernel = np.zeros((1,delta+1))
            
            
        for i in range(x.shape[0]-delta):
            self.buffer.append(self.buffer[-1] + self.kernel @ x[i:i+delta+1])
        return np.concatenate(self.buffer,axis=0)
    def forward(self):
        
        return None
IntegralRect = IntegralRiemann # Define Rect as an alias for Riemann sum