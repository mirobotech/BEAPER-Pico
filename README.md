# BEAPER-Pico

### Beginner Electronics and Programming Educational Robot (BEAPER) for Raspberry Pi Pico

[BEAPER Pico](https://mirobo.tech/beaper) is a circuit kit for learning and teaching beginner microcontroller programming, electronics, and robotics with Raspberry Pi Pico microcontrollers and MicroPython.

This repository contains:

## **/Arduino**

* BEAPERPico.h - C board header file

An example C header file created to allow BEAPER Pico to be programmed using the Arduino IDE and the [arduino-pico core](https://github.com/earlephilhower/arduino-pico).

## **BEAPER_Pico.py**

A MicroPython board support module for BEAPER Pico. Copy BEAPER_Pico.py into the Raspberry Pi Pico filesystem to use it with the Beginner Activities as well as other example programs.

## **/Beginner Activities**
A complete beginner curriculum containing beginner learning activities for BEAPER Pico.

Each beginner activity consists of an example program, Guided Exploration Activities to build understanding, and Extension Activities to practice learned skills. Some beginner activities include additional extension projects.

* BEAPER_Pico.py - BEAPER Pico board support module
* Activity_B01_Output.py - Output, program structure
* Activity_B02_Timing.py - Output with timing (blocking)
* Activity_B03_Input.py - Input programming activity, including logic states
* Activity_B04_Constants_Variables.py - Constants and Variables activity
* B04_Constants_Variables_Exploration.py - Constants and Variables extension project
* Activity_B05_Decision_Structures.py - Decision structures and comparison operators
* Activity_B06_Conditional_Loops.py - Conditional while loops
* Activity_B07_Counted_Loops.py - For loops
* Activity_B08_Functions.py - Creating and using functions
* Activity_B09_Analog_Input.py - Reading and processing analog input values
* Activity_B10_Analog_Output.py - Controlling real-world outputs
* B10_Motor_Controller_Project.py - PWM motor output project
* B10_Servo_Controller_Project.py - Servo output project
* B10_Sound_Controller_Project.py - Sound output project
* Activity_B11_Non-Blocking_Timing.py - Multiple concurrent timers
* B11_Timed_Analog_Output.py - Non-blocking timing project
* Activity_B12_State_Machines.py - A new way to structure programs
* B12_Combination_Lock_Project.py - Digital safe project
* Microcontroller Core Curriculum.md - Curriculum overview
* Numeric Types.md - Numeric types explainer
* Capstone Preparation Guide - Capstone project explainer
* Analog_Monitor.py - Analog monitor capstone project template
* Line_Follower.py - Line following robot capstone project template
* NeoPixel_Controller.py - NeoPixel lighting effects capstone project template
* Simon_Game.py - Memory game capstone project template
* Sumo_Robot.py - Sumo robot capstone project template


## **/LCD**
A MicroPython ST7789 LCD driver module for BEAPER Pico along with example LCD programs.

* LCD.py - MicroPython LCD driver module
* LCDConfig_Pico.py - BEAPER Pico LCD driver configuration file
* LCD_Demo.py - graphics primitives drawing/timing test
* Breakout.py - block breaker game
* Text_Comparison.py - compare built-in font with selected TrueType font
* bar-graph.py - bar graph function module
* Bar_Graph_Demo.py - bar graph demo program
* Fonts - A selection of TrueType fonts converted for use with LCD.py


## **/SONAR**
HC-SR04(P) SONAR module timing test program.

* SONAR_Timing_Test.py - SONAR TRIG -> ECHO delay test


## **/VL53L0X**
A non-blocking VL53L0X ToF (Time of Flight) distance sensor driver module and example programs.

* vl53l0x_nb.py - non-blocking [VL53L0X driver](https://github.com/antirez/VL53L0X.git)
* ToF_SONAR_Comparison.py - VL53L0X/HC-SR04P distance, acquisition time comparison (uses LCD)