import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy
import os
import copy
import re
import math
sensornamedict = {'acc':'ACCELEROMETER',
                  'game_rv':'GAME_ROTATION_VECTOR',
                  'gps':'GPS',
                  'gps_2':'GPS',
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
                    'gps_2':['Time','Latitude','Longitude','Sigma'],
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

def parse_comment(path:str) -> dict:
    # extract commented lines
    with open(path) as file:
        comments = ''
        for line in file:
            if line.startswith('#'):
                comments += line # saves comments as a single string
            else:
                break
    # struct info from comments to dict
    comments = re.split('[\t,\n]',comments) # split strings by sep and newline
    comments = [x.split(': ') for x  in comments if len(x.split(': ')) == 2] # split by ': ' and save to list only when there are two elements. e.g. A: B
    out_dict = {}
    for elem in comments:
        out_dict[elem[0]] = int(elem[1]) if elem[1].isnumeric() else elem[1] # cast the value as integer if value is numeric
    return out_dict

def align_time(time,currenttime,elapsedtime):
    '''
    Align timestamp to elapsed time (nanosec)
    time: array-like object with timestamp as elements
    currenttime: currentTimeMillis
    elapsedtime: elapsedRealtimeNanos
    '''
    bias = currenttime * int(1e6) - elapsedtime
    if len(time) != 0:
        # digit = math.ceil(math.log10(time[0]))
        # if digit == 15:
        #     time_type = 'elapsedRealtimeNanos'
        #     time_new = time
        # elif digit == 13:
        #     time_type = 'currentTimeMillis'
        #     time_new = time*int(1e6) - bias
        # else:
        #     time_type = 'elapsedRealtimeNanos'
        #     time_new = time*int(1e3)
            
        head_index = 3
        currenttime_head = str(currenttime)[:head_index]
        elapsedtime_head = str(elapsedtime)[:head_index]
        time_head = str(time[0])[:head_index]
        while currenttime_head == elapsedtime_head:
            head_index = head_index + 1
            currenttime_head = str(currenttime)[:head_index]
            elapsedtime_head = str(elapsedtime)[:head_index]
            time_head = str(time[0])[:head_index]      
            print(currenttime_head, elapsedtime_head, time_head)
        digit = math.ceil(math.log10(time[0]))
        currenttime_digit = math.ceil(math.log10(currenttime))
        elapsedtime_digit = math.ceil(math.log10(elapsedtime))
        if time_head == currenttime_head:
            time_type = 'currentTimeMillis'
            if digit == currenttime_digit:
                time_new = time * int(1e6) - bias
            else:
                time_new = time * 10**int(currenttime_digit - digit) * int(1e6) - bias
        elif time_head == elapsedtime_head:
            time_type = 'elapsedRealtimeNanos'
            if digit == elapsedtime_digit:
                time_new = time
            else:
                time_new = time * 10**int(elapsedtime_digit - digit)
        else:
            time_new = []
            time_type = ''
    else:
        time_new = []
        time_type = ''
    return time_new, time_type
    
def gps_to_meter(df:pd.DataFrame) -> np.ndarray:
    '''
    df is a pandas.DataFrame object of gps data.
    df should have 3 columns of Time, Lat, Lon. (time, latitude, longitude)
    The index of the df should be pandas.RangeIndex,
    which is default when dataframe is created from pd.read_csv().
    '''
    Latitude = df.Latitude * np.pi / 180
    Longitude = df.Longitude * np.pi / 180
    d_lat = np.array(Latitude - Latitude[0])
    d_lon = np.array(Longitude - Longitude[0])
    d_y = np.multiply(np.array(d_lat)*180/np.pi,
                      (111132.954 - 559.822*np.cos(2*Latitude[0]) + 1.175*np.cos(4*Latitude[0]) - 0.0023*np.cos(6*Latitude[0])))
    d_x = np.multiply(np.array(d_lon)*180/np.pi,
                      (111412.84*np.cos(Latitude) - 93.5*np.cos(Latitude) + 0.118*np.cos(5*Latitude)))
    out = np.stack([d_x, d_y],axis=1)
    return (out)