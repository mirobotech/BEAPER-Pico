## VL53L0X

A non-blocking MicroPython program and example programs for use with VL53L0X ToF (Time-of-Flight) LASER distance sensor modules and the BEAPER Pico circuit.

* Sensors_Demo.py - a demo program using BEAPER Pico's LCD to show a radar-like parameter display including floor sensor reflectivity, Raspberry Pi Pico system input voltage, Raspberry Pi Pico die temperature, and distance read from either: HC-SR04P SONAR distance sensor module, VL53L0X ToF (Time-of-Flight) LASER distance sensor module, or VL53L4CD ToF LASER distance sensor module.
* ToF_SONAR_Comparison.py - a demo program using BEAPER Pico's LCD to compare VL53L0X ToF and HC-SR04P SONAR distance and measurement time with a graphical oscilloscope view of the SONAR TRIG and ECHO signals.
* ToF_test.py - a non-blocking distance measurement test
* vl53l0x_nb.py - a non-blocking [VL53L0X driver from Antirez](https://github.com/antirez/VL53L0X.git)

