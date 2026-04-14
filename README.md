# BEAPER-Pico

## Beginner Electronics and Programming Educational Robot (BEAPER) for Raspberry Pi Pico

[BEAPER Pico](https://mirobo.tech/beaper) is a beginner circuit kit for learning and teaching microcontroller programming and robotics using Raspberry Pi Pico microcontrollers.

This repository contains:
* Arduino - a header file for programming BEAPER Pico using the Arduino IDE
* Beginner Activities - example programs comprising a complete beginner course for teaching Raspberry Pi Pico programming in MicroPython using BEAPER Pico
* LCD - a MicroPython ST7789 LCD driver module and example programs
* VL53L0X - a VL53L0X ToF (Time of Flight) distance sensor driver module and example programs

## Beginner Activities - Beginner learning activities

Each beginner activity contains an example program, Guided Exploration Activities to build understanding, and Extension Activities to practice learned skills.

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

## LCD - MicroPython ST7789 LCD Driver Module

* LCD.py - MicroPython LCD driver module
* LCDConfig_Pico.py - BEAPER Pico LCD driver configuration file
* LCD_Demo.py - graphics primitives drawing/timing test
* Breakout.py - block breaker game
* Text_Comparison.py - compare built-in font with selected TrueType font
* bar-graph.py - bar graph function module
* Bar_Graph_Demo.py - bar graph demo program
* Fonts - Various TrueType fonts converted for use with LCD.py

## VL53L0X - Non-blocking ToF Driver Module

* vl53l0x_nb.py - non-blocking [VL53L0X driver](https://github.com/antirez/VL53L0X.git)
* BEAPER_Pico.py - BEAPER Pico board support module
* ToF_SONAR_Comparison.py - Distance, acquisition time comparison (uses LCD)
* ToF_Robot.py - BEAPER Pico robot using either non-blocking VL53L0X distance sensing or SONAR distance sensing