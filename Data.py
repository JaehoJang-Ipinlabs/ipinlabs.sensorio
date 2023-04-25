# Dependencies
import copy # python standard library
import warnings # python standard library
import numpy as np # NumPy library. "pip install numpy" or "conda install numpy"

# Class definitions
class Data:
    '''
    Data class is a base class for SensorData and AndroidData class.
    '''
    def __init__(self):
        pass
    def _to_csv(self):
        '''
        Export values to a csv file.
        '''
        # This method is not implemented yet!
        # Delete warning below when this method is fully implemented.
        warnings.warn('This method is on development!')
    def _to_feather(self):
        '''
        Export values to a feather file.
        '''
        # This method is not implemented yet!
        # Delete warning below when this method is fully implemented.
        warnings.warn('This method is on development!')
    def _to_parquet(self):
        '''
        Export values to a parquet file.
        '''
        # This method is not implemented yet!
        # Delete warning below when this method is fully implemented.
        warnings.warn('This method is on development!')
    def _to_pickle(self):
        '''
        Save instance to a pickle file.
        '''
        # This method is not implemented yet!
        # Delete warning below when this method is fully implemented.
        warnings.warn('This method is on development!')

class SensorData(Data):
    '''
    SensorData class is a class to store and utilize data from android smartphone sensors.
    The stored values are never accessed directly. Only the deep copied instances are returned.
    '''
    def __init__(self, data=None, time=None):
        self.__data = None # attribute 'data' initialize. The getter will return None if value is not assigned.
        self.__time = None # attribute 'time' initialize. The getter will return None if value is not assigned.
        self.data = data # input parameter 'data' is deep copied and assigned to attribute 'data'.
        self.time = time # input parameter 'time' is deep copied and assigned to attribute 'time'.
    def load(self, file):
        '''
        Load sensor timestamp and values from a file.
        '''
        # This method is not implemented yet!
        # Delete warning below when this method is fully implemented.
        warnings.warn('This method is on development!')
    def assign(self, obj):
        '''
        Assign given sensor timestamp and values.
        '''
        # Insert type validation process of obj variable here
        # Insert value and time assignment process using getters here
        # This method is not implemented yet!
        # Delete warning below when this method is fully implemented.
        warnings.warn('This method is on development!')
    @property
    def data(self):
        '''
        getter method for the data attribute.
        '''
        return copy.deepcopy(self.__data) # return deep copied instant
    @data.setter
    def data(self, value):
        '''
        setter method for the data attribute.
        '''
        # Insert validation process here.
        self.__data = copy.deepcopy(value) # store deep copied instant
    @data.deleter
    def data(self):
        '''
        deleter method for the data attribute.
        '''
        # Warnings for deleting data attribute. Other methods and functions will expect data attribute to exist.
        warnings.warn('data attirubte must be reassigned before using this instance!')
        # Insert logging function if tracking is needed.
        del self.__data
    @property
    def time(self):
        '''
        getter method for the time attribute.
        '''
        return copy.deepcopy(self.__time) # return deep copied instant
    @time.setter
    def time(self, value):
        '''
        setter method for the time attribute.
        '''
        # Insert validation process here.
        # Validation for Uniqueness.
        '''
        if not(exist duplicate) then is_unique = True
        else is_unique = False
        '''
        # Exception handling for Uniqueness (There exist duplicate time stamp).
        '''
        if not(is_unique) then remove duplicate(time, data)
        '''
        # Validation for Monotonic increase.
        '''
        if all(time > L[time]) then is_monotonic_increase = True
        else is_monotonic_incrase = False
        '''
        # Exception handling for Monotonic increase (The order of time stamp is not temporal).
        '''
        if not(is_monotonic_increase) then sort(time, data)
        '''
        self.__time = copy.deepcopy(value) # store deep copied instant
        # This method is not implemented yet!
        # Delete warning below when this method is fully implemented.
        warnings.warn('This method is on development!')
    @time.deleter
    def time(self):
        '''
        deleter method for the time attribute.
        '''
        # Warnings for deleting time attribute. Other methods and functions will expect time attribute to exist.
        warnings.warn('time attirubte must be reassigned before using this instance!')
        # Insert logging function if tracking is needed.
        del self.__time

class AndroidData(Data):
    '''
    AndroidData class is a class to store and utilize multiple SensorData in a single instance. The SensorData instance should be unique for each sensor types. e.g. There should not exist multiple TYPE_ACCELEROMETER data.
    '''
    def __init__(self):
        pass
    def save(self,obj):
        # Delete or modify this method.
        '''
        Dummy method to assign value to attribute.
        '''
        self.data.append(obj)
        return None
    def __add__(self,other):
        # Delete or modify this method.
        '''
        Dummy method for debugging purpose, which overrides + operator to behave as concatenate function.
        '''
        if type(other) != type(self):
            raise TypeError('Addition between AndroidData and {} is not supported.'.format(type(other)))
        out = AndroidData()
        out.data = self.data + other.data
        return out