# BEAPER-Pico

## Beginner Electronics and Programming Educational Robot (BEAPER) for Raspberry Pi Pico

[BEAPER Pico](https://mirobo.tech/beaper) is a beginner circuit kit for learning and teaching with Raspberry Pi Pico microcontrollers.

This repository contains:
* Beginner Activities - NEW learning activities
* Introductory Programming Activities - Old
* a MicroPython ST7789 LCD driver module and example programs
* a VL53L0X ToF (Time of Flight) driver module and example programs

## Beginner Activities - New beginner learning activities

* BEAPER_Pico.py - BEAPER Pico board support module
* Activity_B01_Output.py - Output, program structure
* Activity_B02_Timing.py - Output with timing (blocking)
* Activity_B03_Input.py - Input programming activity, including logic states
* Activity_B04_Constants_Variables.py - Constants and Variables activity
* B04_Constants_Variables_Exploration.py - Constants and Variables extension project
* Activity_B05_Decision_Structures.py - Decision structures and comparison operators


## Introductory Programming Activities - Older beginner programming activities

* BEAPER-Pico-Intro-1.py - Input and output programs, including if conditions, logical conditions, simple sounds, and the creation of a start-stop pushbutton circuit and bicycle turn signals.
* BEAPER-Pico-Intro-2.py - Variable and constant programming, including the creation of a toggle button and a two-player rapid-clicker game.
* BEAPER-Pico-Intro-3.py - Loops, including while and for loops, and an introduction to PWM.
* BEAPER-Pico-Intro-4.py - Functions, including parameter passing and an Arduino-like tone() function.
* BEAPER-Pico-Intro-5.py - Analog input, print output for debugging, f-string formatting, and a map() function.

## LCD - MicroPython ST7789 LCD Driver Module

* LCD.py - MicroPython LCD driver module
* LCDConfig_Pico.py - BEAPER Pico LCD driver configuration file
* LCDdemo.py - Graphics primitives drawing test
* Breakout.py - Block breaker game
* Fonts - Various fonts converted for use with LCD.py

## VL53L0X - Non-blocking ToF Driver Module

* vl53l0x_nb.py - [Non-blocking VL53L0X driver](https://github.com/antirez/VL53L0X.git)
* BEAPER_Pico.py - BEAPER Pico board support module
* ToF_SONAR_Comparison.py - Distance, acquisition time comparison (uses LCD)
* ToF_Robot.py - BEAPER Pico robot using either non-blocking VL53L0X distance sensing code or SONAR distance sensing