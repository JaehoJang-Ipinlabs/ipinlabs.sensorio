import pandas as pd
import matplotlib.pyplot as plt
import os
sensornamedict = {'acc':'ACCELEROMETER',
                  'game_rv':'GAME_ROTATION_VECTOR',
                  'gps':'GPS',
                  'gravity':'GRAVITY',
                  'gyro':'GYROSCOPE',
                  'gyro_uncalib':'GYROSCOPE_UNCALIBRATED',
                  'linacc':'LINEAR_ACCELERATION',
                  'magnet':'MAGNETIC_FIELD',
                  'magnet_uncalib':'MAGNETIC_FIELD_UNCALIBRATED',
                  'pressure':'PRESSURE',
                  'ronin':'RONIN',
                  'rv':'ROTATION_VECTOR',
                  'step':'STEP',
                  'wifi':'WIFI'}
sensorcolumndict = {'acc':['Time','X','Y','Z'],
                    'game_rv':['Time','X','Y','Z','W'],
                    'gps':['Time','Latitude','Longitude'],
                    'gravity':['Time','X','Y','Z'],
                    'gyro':['Time','X','Y','Z'],
                    'gyro_uncalib':['Time','X_uncalib','Y_uncalib','Z_uncalib','X_drift','Y_drift','Z_drift'],
                    'linacc':['Time','X','Y','Z'],
                    'magnet':['Time','X','Y','Z'],
                    'magnet_uncalib':['Time','X_uncalib','Y_uncalib','Z_uncalib','X_bias','Y_bias','Z_bias'],
                    'pressure':['Time','Pressure'],
                    'ronin':['Time','X','Y'],
                    'rv':['Time','X','Y','Z','W','Var_Unknown_placeholder'],
                    'step':['Time','Step'],
                    'wifi':['Time','Mac','RSSI','Var_Unknown_placeholder','SSID']}

def sensorparser(path):
    # extract info from commented lines
    
    # extract data from regular lines
    return None

class FileFromCsv:
    def __init__(self,path,opt = None):
        self.__filename = path.split('/')[-1][:-4] # extract file name excluding the extension
        self.__sensortype = sensornamedict[self.__filename]
        self.__dataframe = pd.read_csv(path, names=sensorcolumndict[self.__filename]) if opt is None else pd.read_csv(path,names=sensorcolumndict[self.__filename],**opt)
    @property
    def filename(self):
        return self.__filename
    @property
    def sensortype(self):
        return self.__sensortype
    @property
    def dataframe(self):
        return self.__dataframe.copy(deep=True)
    @dataframe.setter
    def dataframe(self,df):
        self.__dataframe = df.copy(deep=True)
    @dataframe.deleter
    def dataframe(self):
        del self.__dataframe
    def __str__(self):
        out = str(self.dataframe)
        return(out) # to be implemented
    def __repr__(self):
        out = str(self.dataframe)
        return(out) # to be implemented
    def _repr_html_(self):
        out = self.dataframe._repr_html_()
        return(f'{out}') # to be implemented
    
class TrialFromCsv:
    def __init__(self, path, opt = {'header' : None, 'comment' : '#', 'sep' : '\t'}):
        self.__path = path
        self.opt = opt
        self.sensors = {} # List of FileFromCsv? or dict?
        self.read_csvs()
    @property
    def path(self):
        return self.__path    
    def get_sensors(self):
        return list(self.sensors.keys())
    def get_csvlist(self,ext = 'txt'): # return list of file path ends with specific extension
        filelist = []
        for file in os.listdir(self.path):
            if file.endswith('.'+ext):
                filelist.append(os.path.join(self.path,file))
        return filelist
    def read_csvs(self,ext = 'txt'):
        for file in self.get_csvlist(ext):
            data = FileFromCsv(file,self.opt)
            self.sensors[data.sensortype] = data
        return None
    def describe_time(self,plot : bool = True):
        times = [x.dataframe.Time for x in self.sensors.values()]
        sensor_types = [x.sensortype for x in self.sensors.values()]
        desc = [x.describe() for x in times]
        if plot:
            fig = plt.figure()
            ax = fig.add_axes((1,1,1,1))
            ax.boxplot(times)
            ax.set_xticklabels(sensor_types, rotation = 90)
            ax.grid()
        return times, sensor_types, desc
    def describe_interval(self):
        intervals = [x.dataframe.Time.diff(axis=0) for x in self.sensors.values()]
        desc = [x.describe() for x in intervals]
        return desc