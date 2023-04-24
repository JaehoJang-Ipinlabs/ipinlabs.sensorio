# AndroidSensorData
Python class for android smartphone's sensor data

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
|---|:---:|:---:|:---:|:---:|
|[TYPE_ACCELEROMETER](#type_accelerometer)|                 <b>Yes</b>|<b>Yes</b>|<b>Yes</b>|<b>Yes</b>|
|[TYPE_AMBIENT_TEMPERATURE](#type_ambient_temperature)|     <b>Yes</b>|<I>n/a</I>|<I>n/a</I>|<I>n/a</I>|
|[TYPE_GRAVITY](#type_gravity)|                             <b>Yes</b>|<b>Yes</b>|<I>n/a</I>|<I>n/a</I>|
|[TYPE_GYROSCOPE](#type_gyroscope)|                         <b>Yes</b>|<b>Yes</b>|<I>n/a</I>|<I>n/a</I>|
|[TYPE_LIGHT](#type_light)|                                 <b>Yes</b>|<b>Yes</b>|<b>Yes</b>|<b>Yes</b>|
|[TYPE_LINEAR_ACCELERATION](#type_linear_acceleration)|     <b>Yes</b>|<b>Yes</b>|<I>n/a</I>|<I>n/a</I>|
|[TYPE_MAGNETIC_FILED](#type_magnetic_field)|               <b>Yes</b>|<b>Yes</b>|<b>Yes</b>|<b>Yes</b>|
|TYPE_ORIENTATION<sup>1</sup>|                              <b>Yes</b>|<b>Yes</b>|<b>Yes</b>|<b>Yes</b>|
|[TYPE_PRESSURE](#type_pressure)|                           <b>Yes</b>|<b>Yes</b>|<I>n/a</I>|<I>n/a</I>|
|[TYPE_PROXIMITY](#type_proximity)|                         <b>Yes</b>|<b>Yes</b>|<b>Yes</b>|<b>Yes</b>|
|[TYPE_RELATIVE_HUMIDITY](#type_relative_humidity)|         <b>Yes</b>|<I>n/a</I>|<I>n/a</I>|<I>n/a</I>|
|[TYPE_ROTATION_VECTOR](#type_rotation_vector)|             <b>Yes</b>|<b>Yes</b>|<I>n/a</I>|<I>n/a</I>|
|TYPE_TEMPERATURE<sup>1</sup>|                              <b>Yes</b>|<b>Yes</b>|<b>Yes</b>|<b>Yes</b>|

<sup>1</sup>This sensor is deprecated.

### Sensor Coordinate System
<img src="https://developer.android.com/static/images/axis_device.png" title="Device_Axis"></img> <br>
This coordinate is applied to: <br>
* [Acceleration Sensor](#type_accelerometer) <br>
* Gravity Sensor <br>
* Gyroscope <br>
* Linear Acceleration Sensor <br>
* Geomagnetic Field Sensor <br>

### Sensor Description and Units of Measure
#### TYPE_ACCELEROMETER
#### TYPE_AMBIENT_TEMPERATURE
#### TYPE_GRAVITY
#### TYPE_GYROSCOPE
#### TYPE_LIGHT
#### TYPE_LINEAR_ACCELERATION
#### TYPE_MAGNETIC_FILED
#### TYPE_PRESSURE
#### TYPE_PROXIMITY
#### TYPE_RELATIVE_HUMIDITY
#### TYPE_ROTATION_VECTOR
