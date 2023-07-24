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

class SensorData():
    '''
    SensorData class is a class to store and utilize data from android smartphone sensors.
    The stored values are never accessed directly. Only the deep copied instances are returned.
    '''
    def __init__(self, path : str, opt : dict = {'sep':'\t', 'header':None, 'comment':'#', 'index_col':False}):
        self.__filename = path.split('/')[-1][:-4] # extract file name excluding the extension
        self.__sensortype = sensornamedict[self.__filename]
        if opt is None:
            self.__dataframe = pd.read_csv(path, names=sensorcolumndict[self.__filename])
            if self.__filename == 'gps' and not isinstance(self.__dataframe.index, pd.RangeIndex):
                self.__filename = 'gps_2'
                self.__dataframe = pd.read_csv(path,names=sensorcolumndict[self.__filename])
        else:
            self.__dataframe = pd.read_csv(path,names=sensorcolumndict[self.__filename],**opt)
            if self.__filename == 'gps' and not isinstance(self.__dataframe.index, pd.RangeIndex):
                self.__filename = 'gps_2'
                self.__dataframe = pd.read_csv(path,names=sensorcolumndict[self.__filename],**opt)
        self.__dataframe.name = self.__filename
        self.__comment = utils.parse_comment(path)
        self.__time = self.dataframe.Time
        time_new, self.time_type = utils.align_time(self.__time,self.comment['currentTimeMillis'],self.comment['elapsedRealtimeNanos'])
        self.__dataframe['Time'] = time_new
    @property
    def dataframe(self):
        out = self.__dataframe.copy(deep=True)
        out.name = self.__dataframe.name
        return out
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
        self.interpolate()
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
            if (len(list(self.sensors.values())[i].dataframe.Time) > 0) and (list(self.sensors.keys())[i] != 'WIFI'):
                interpolator = scipy.interpolate.interp1d(list(self.sensors.values())[i].dataframe.iloc[:,0],list(self.sensors.values())[i].dataframe.iloc[:,1:],axis=0)
                data_new = pd.DataFrame(np.concatenate([np.expand_dims(time_new,axis=1), interpolator(time_new)],axis=1),columns=list(self.sensors.values())[i].dataframe.columns)
                data_new.name = list(self.sensors.values())[i].dataframe.name
                self.interpolated[list(self.sensors.keys())[i]] = data_new
        return None
    def fft(self):
        for i in range(len(self.interpolated.values())):
            val = list(self.interpolated.values())[i].iloc[:,1:]
            freq = []
            sp = []
            for c in range(val.shape[1]):
                freq.append(np.fft.fftfreq(n=len(val.iloc[:,c]),d=self.dt*1e-9))
                sp.append(np.fft.fft(val.iloc[:,c]))
            self.freq[list(self.interpolated.keys())[i]] = np.stack(freq,axis=0)
            self.sp[list(self.interpolated.keys())[i]] = np.stack(sp,axis=0)
        return None
        
def load_from_directory(path: str):
    '''
    A function which loads multiple sensor data under the directory of given path.
    path (str) : A path to data directory.
    '''
    
    data = TrialData()
    return data