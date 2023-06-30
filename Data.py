# Dependencies
import copy # python standard library
import warnings # python standard library
import os # python standard library
import numpy as np # NumPy library. "pip install numpy"
import pandas as pd # Pandas library. "pip install pandas"
import scipy # scipy library. "pip install scipy"
import matplotlib.pyplot as plt # matplotlib library. "pip install matplotlib"
import ipinlabs.sensorio.utils as utils

sensornamedict = utils.sensornamedict
sensorcolumndict = utils.sensorcolumndict

# Class definition for trial listing
# class DataList:
#     '''
#     DataList class is a class for listing all the trials under the given path.
#     '''
#     def __init__(self,path=None):
#         self.__path = path
#         self.__trial = None
#     def __str__(self):
#         if self.__trial is None:
#             return ('None')
#         else:
#             return(str(list(self.__trial)))
#     def __repr__(self):
#         return ('DataList(\''+str(self.__path)+'\')')
#     def get_trials(self):
#         if self.__path is None:
#             raise Exception('Trial path is not assigned. Assign trial directory path via DataList.setpath()')
#         else:
#             if self.__trial is None:
#                 self.__update()
#             else:
#                 pass
#             return self.__trial
#     def setpath(self,path):
#         self.__path = path
#         self.__update()    
#     def __update(self):
#         if self.__path is None:
#             raise Exception('DataList.update is called without proper trial directory path. Assign trial directory path via DataList.setpath()')
#         else:
#             self.__trial = os.listdir(self.__path)

# Class definitions
# class Data:
#     '''
#     Data class is a base class for SensorData and TrialData class.
#     '''
#     def __init__(self):
#         self.__data = None # attribute 'data' initialize. The getter will return None if value is not assigned.
#     def __str__(self):
#         out = str(self.data)
#         return(out) # to be implemented
#     def __repr__(self):
#         out = str(self.data)
#         return(out) # to be implemented
#     def _repr_html_(self):
#         out = self.data._repr_html_()
#         return(f'{out}') # to be implemented
#     @property
#     def data(self):
#         '''
#         getter method for the data attribute.
#         '''
#         return copy.deepcopy(self.__data) # return deep copied instant
#     @data.setter
#     def data(self, value):
#         '''
#         setter method for the data attribute.
#         '''
#         # Insert validation process here.
#         self.__data = copy.deepcopy(value) # store deep copied instant
#     @data.deleter
#     def data(self):
#         '''
#         deleter method for the data attribute.
#         '''
#         # Warnings for deleting data attribute. Other methods and functions will expect data attribute to exist.
#         warnings.warn('data attribute must be reassigned before using this instance!')
#         # Insert logging function if tracking is needed.
#         del self.__data
#     def _to_csv(self):
#         '''
#         Export values to a csv file.
#         '''
#         # This method is not implemented yet!
#         # Delete warning below when this method is fully implemented.
#         warnings.warn('This method is on development!')
#     def _to_feather(self):
#         '''
#         Export values to a feather file.
#         '''
#         # This method is not implemented yet!
#         # Delete warning below when this method is fully implemented.
#         warnings.warn('This method is on development!')
#     def _to_parquet(self):
#         '''
#         Export values to a parquet file.
#         '''
#         # This method is not implemented yet!
#         # Delete warning below when this method is fully implemented.
#         warnings.warn('This method is on development!')
#     def _to_pickle(self):
#         '''
#         Save instance to a pickle file.
#         '''
#         # This method is not implemented yet!
#         # Delete warning below when this method is fully implemented.
#         warnings.warn('This method is on development!')
    

class SensorData():
    '''
    SensorData class is a class to store and utilize data from android smartphone sensors.
    The stored values are never accessed directly. Only the deep copied instances are returned.
    '''
    def __init__(self, path : str, opt : dict = {'sep':'\t', 'header':None, 'comment':'#'}):
        self.__filename = path.split('/')[-1][:-4] # extract file name excluding the extension
        self.__sensortype = sensornamedict[self.__filename]
        if opt is None:
            self.__dataframe = pd.read_csv(path, names=sensorcolumndict[self.__filename])
        else:
            self.__dataframe = pd.read_csv(path,names=sensorcolumndict[self.__filename],**opt)
        self.__comment = utils.parse_comment(path)
        self.__time = self.dataframe.Time
        time_new, self.time_type = utils.align_time(self.__time,self.comment['currentTimeMillis'],self.comment['elapsedRealtimeNanos'])
        self.__dataframe['Time'] = time_new
    @property
    def dataframe(self):
        return self.__dataframe.copy(deep=True)
    @property
    def comment(self):
        return copy.deepcopy(self.__comment)
    @property
    def sensortype(self):
        return copy.deepcopy(self.__sensortype)

class TrialData():
    '''
    TrialData class is a class to store and utilize multiple SensorData
    from an identical trial in a single instance. The SensorData instance
    should be unique for each sensor types. e.g. There should not exist
    multiple TYPE_ACCELEROMETER data.
    '''
    def __init__(self, path : str, opt : dict = {'header' : None, 'comment' : '#', 'sep' : '\t'}, dt : int = int(1e6)):
        self.__path = path
        self.opt = opt
        self.sensors = {} # List of FileFromCsv? or dict?
        self.interpolated = {}
        self.freq = {}
        self.sp = {}
        self.read_csvs() # Modify self.sensors (load from files)
        self.timeinfo = self.inspect_time()
        self.dt = dt
    @property
    def path(self):
        return self.__path
    def get_sensors(self):
        return list(self.sensors.keys())
    def get_csvlist(self, ext : str = 'txt'): # return list of file path ends with specific extension
        filelist = []
        for file in os.listdir(self.path):
            if file.endswith('.'+ext):
                filelist.append(os.path.join(self.path,file))
        return filelist
    def read_csvs(self, ext : str = 'txt'):
        for file in self.get_csvlist(ext):
            data = SensorData(file,self.opt)
            self.sensors[data.sensortype] = data
        return None
    def describe_time(self, plot : bool = True):
        start_times = [x.comment['elapsedRealtimeNanos'] for x in self.sensors.values()]
        start_time = start_times[0] if start_times.count(start_times[0]) == len(start_times) else None
        if start_time is None:
            raise Exception('Measurement start time in elapsedRealtimeNanos are not identical.')
        times = [x.dataframe.Time for x in self.sensors.values()]
        sensor_types = [x.sensortype for x in self.sensors.values()]
        desc = [x.describe() for x in times]
        # measuremnt time period box plot
        if plot:
            fig = plt.figure()
            ax = fig.add_axes((1,1,1,1))
            ax.boxplot(times)
            ax.axhline(start_time,color = 'k',ls = ':')
            for id, time in enumerate(times):
                if len(time)==0:
                    ax.axvspan(id+.5, id+1.5, alpha = .5, color='grey')
            ax.set_xticklabels(sensor_types, rotation = 90)
            ax.grid()
            ax.set_title('Timestamp distribution')
            return times, sensor_types, desc, fig
        else:
            return times, sensor_types, desc
    def describe_interval(self, plot : bool = True):
        intervals = [pd.Series(x.dataframe.Time.unique()).diff().iloc[1:] if len(x.dataframe.Time)>0 else pd.Series(dtype=float) for x in self.sensors.values()]
        desc = [x.describe() for x in intervals]
        sensor_types = [x.sensortype for x in self.sensors.values()]
        # measurement time interval box plot
        if plot:
            fig = plt.figure()
            ax = fig.add_axes((1,1,1,1))
            ax.boxplot(intervals)
            for id, interval in enumerate(intervals):
                if len(interval) == 0:
                    ax.axvspan(id+.5, id+1.5, alpha=.5, color='grey')
            ax.set_xticklabels(sensor_types, rotation = 90)
            ax.grid()
            ax.set_yscale('log')
            ax.set_title('Time interval distribution')
        return desc, fig
    def inspect_time(self,idx : int = None):
        time_info = self.describe_time(plot = False)
        if idx is None:
            return time_info
        elif (type(idx) is int) and (idx < 3):
            return time_info[idx]
        else:
            raise Exception('idx error. idx should be either integer.')
    def interpolate(self):
        time_min = int(np.max([x.loc['min'] if not(np.isnan(x.loc['min'])) else -np.inf for x in self.inspect_time(2)])) # get latest time among starting times
        time_max = int(np.min([x.loc['max'] if not(np.isnan(x.loc['max'])) else np.inf for x in self.inspect_time(2)])) # get earliest time among ending times
        time_new = np.arange(time_min, time_max, self.dt)
        for i in range(len(self.sensors.values())):
            if len(list(self.sensors.values())[i].dataframe.Time) > 0:
                interpolator = scipy.interpolate.interp1d(list(self.sensors.values())[i].dataframe.iloc[:,0],list(self.sensors.values())[i].dataframe.iloc[:,1:],axis=0)
                data_new = pd.DataFrame(np.concatenate([np.expand_dims(time_new,axis=1), interpolator(time_new)],axis=1),columns=list(self.sensors.values())[i].dataframe.columns)
                self.interpolated[list(self.sensors.keys())[i]] = data_new
        return self.interpolated
    def fft(self):
        for i in range(len(self.interpolated.values())):
            
            self.freq[list(self.interpolated.keys())[i]] = np.fft.fftfreq(list(self.interpolated.values())[i].dataframe.iloc[:,1:])
            self.sp[list(self.interpolated.keys())[i]] = np.fft.fft(list(self.interpolated.values())[i].dataframe.iloc[:,1:])
        
        
def load_from_directory(path: str):
    '''
    A function which loads multiple sensor data under the directory of given path.
    path (str) : A path to data directory.
    '''
    
    data = TrialData()
    return data