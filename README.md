# AndroidSensorData
Python class for android smartphone's sensor data

## Table of Contents
[1. License](#license) <br>
[2. Classes](#classes) <br>
[3. Functions](#functions) <br>
[4. Android Sensors](#android_sensors) <br>
  [4.1. Supported Sensors by Platform]()

## License
Codes of this repository is made available to you under : <br>
[GNU General Public License v3.0](https://github.com/JaehoJang-Ipinlabs/AndroidSensorData/blob/main/LICENSE) <br>
<br>
[Documentation of android sensors](#android-sensors-see-official-guide-for-more-informations) is made available to you under : <br>
[Apache 2.0 license](https://www.apache.org/licenses/LICENSE-2.0)

## Classes
<b>class</b> <I>SensorData</I> <br>
Class that stores each individual sensor's data and timestamp

<b>class</b> <I>AndroidData</I> <br>
Class that stores multiple SensorData. SensorData is unique for each sensor types. 

## Functions

## Android Sensors (see [official guide](https://developer.android.com/guide/topics/sensors/sensors_overview) for more informations.)
### Supported sensors by platform
|Sensor|Android 4.0 <br> API Level 14|Android 2.3 <br> API Level 9|Android 2.2 <br> API Level 8|Android 1.5 <br> API Level 3|
|---|---|---|---|---|
|TYPE_ACCELEROMETER|Yes|Yes|Yes|Yes|
