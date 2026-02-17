"""
================================================================================
ToF_Robot.py]
February 16, 2026

Platform: mirobo.tech BEAPER Pico circuit
Requires: BEAPER_Pico.py board module file
          vl53l0x_nb.py non-blocking VL53L0X driver module

Table-top robot using ToF target finding and floor sensor edge detection.
================================================================================
"""

# --- MicroPython Modules --------------
from machine import Pin, PWM, I2C, ADC
import time

# VL53L0X module
from vl53l0x_nb import VL53L0X
# BEAPER Pico module
import BEAPER_Pico as beaper

# --- Program Constants ----------------
MAX_TARGET_RANGE = const(500)   # Follow targets within max range (mm)
DARK_THRESHOLD = const(40000)   # Floor sensor dark threshold
REV_TIME = const(200)           # Reversing time (ms)

# --- Program Variables ----------------
sonar_mode = False
sonar_range_mm = 0
sonar_time_us = 0
tof_mode = False
tof_range_mm = 0
tof_time_us = 0


# I2C is configured in BEAPER_Pico module
# QWIIC = I2C(id=beaper.I2C_ID, sda=beaper.SDA, scl=beaper.SCL)
# VL53L0X device should answer I2C scan at address 41
# print("I2C scan:", i2c.scan())
tof = VL53L0X(beaper.QWIIC)
# Start first range request (non-blocking)
tof.start_range_request()

while True:
    SW2_pressed = (beaper.SW2.value() == 0)
    SW3_pressed = (beaper.SW3.value() == 0)
    SW4_pressed = (beaper.SW4.value() == 0)
    SW5_pressed = (beaper.SW5.value() == 0)
    
    # Start robot in ToF mode
    if SW3_pressed:
        tof_mode = True
        beaper.pico_led_on()

    # Start robot in SONAR mode
    if SW4_pressed:
        sonar_mode = True
        beaper.pico_led_on()

    # Stop robot to change modes
    if SW5_pressed:
        tof_mode = False
        sonar_mode = False
        beaper.pico_led_off()
        
    if not (tof_mode or sonar_mode):
        time.sleep_ms(10)
       
    while sonar_mode:
        sonar_range_mm = beaper.sonar_distance_cm()
        if sonar_range_mm > 0:
            sonar_range_mm = int(sonar_range_mm*10)
        else:
            time.sleep_ms(10)
        
        if 0 < sonar_range_mm < MAX_TARGET_RANGE:
            beaper.left_motor_forward()
            beaper.right_motor_forward()
        else:
            beaper.left_motor_forward()
            beaper.right_motor_reverse()
            
        if beaper.Q1_level() < DARK_THRESHOLD:
            beaper.motors_stop()
            time.sleep_ms(1)
            beaper.left_motor_reverse()
            while beaper.Q1_level() < DARK_THRESHOLD:
                pass
            beaper.right_motor_reverse()
            time.sleep_ms(REV_TIME)
            
        if beaper.Q3_level() < DARK_THRESHOLD:
            beaper.motors_stop()
            time.sleep_ms(1)
            beaper.right_motor_reverse()
            while beaper.Q3_level() < DARK_THRESHOLD:
                pass
            beaper.left_motor_reverse()
            time.sleep_ms(REV_TIME)
            
        SW5_pressed = (beaper.SW5.value() == 0)
        if SW5_pressed:
            beaper.motors_stop()
            sonar_mode = False
        
            
    while tof_mode:
        if tof.reading_available():
            tof_range_mm = tof.get_range_value()-30
            tof.start_range_request()
        
        if 0 < tof_range_mm < MAX_TARGET_RANGE:
            beaper.left_motor_forward()
            beaper.right_motor_forward()
        else:
            beaper.left_motor_forward()
            beaper.right_motor_reverse()
            
        if beaper.Q1_level() < DARK_THRESHOLD:
            beaper.motors_stop()
            time.sleep_ms(1)
            beaper.left_motor_reverse()
            while beaper.Q1_level() < DARK_THRESHOLD:
                pass
            beaper.right_motor_reverse()
            time.sleep_ms(REV_TIME)
            
        if beaper.Q3_level() < DARK_THRESHOLD:
            beaper.motors_stop()
            time.sleep_ms(1)
            beaper.right_motor_reverse()
            while beaper.Q3_level() < DARK_THRESHOLD:
                pass
            beaper.left_motor_reverse()
            time.sleep_ms(REV_TIME)
            
        SW5_pressed = (beaper.SW5.value() == 0)
        if SW5_pressed:
            beaper.motors_stop()
            tof_mode = False
                
