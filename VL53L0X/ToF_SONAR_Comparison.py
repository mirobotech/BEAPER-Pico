"""
================================================================================
ToF_SONAR_Comparison.py
February 16, 2026

Platform: mirobo.tech BEAPER Pico circuit
Requires: BEAPER_Pico.py board support module file
          vl53l0x_nb.py non-blocking VL53L0X driver module
          LCDconfig_Pico.py LCD driver module
          RedditSans_24.py font module

Compares distance and ranging acquisition time for VL53L0X ToF (Time of Flight)
and HC-SR04P SONAR distance sensor modules.
================================================================================
"""

# --- MicroPython Modules --------------
from machine import Pin, I2C
import framebuf
import array
import time

# LCD driver module
import LCDconfig_Pico as lcd_config
# Font module
import RedditSans_24 as rs24
# VL53L0X module
from vl53l0x_nb import VL53L0X
# BEAPER Pico support module
import BEAPER_Pico as beaper

# --- Program Variables ----------------
sonar_range_mm = 0
sonar_time_us = 0
tof_range_mm = 0
tof_time_us = 0

beaper.pico_led_on()

# I2C is configured in BEAPER_Pico module
# QWIIC = I2C(id=beaper.I2C_ID, sda=beaper.SDA, scl=beaper.SCL)
# VL53L0X device should answer I2C scan at address 41
# print("I2C scan:", beaper.QWIIC.scan())
tof = VL53L0X(beaper.QWIIC)

# Configure LCD (rotation=3 is 'up' for BEAPER Pico LCD)
lcd = lcd_config.config(rotation=3)

# Write LCD headings into LCD framebuffer
lcd.fill(0x0)
lcd.write("VL53L0X", 0, 0, rs24, lcd.WHITE, None)
lcd.write("HC-SR04P", 120, 0, rs24, lcd.WHITE, None)

while True:
    # Measure time to get SONAR range
    sonar_start = time.ticks_us()
    sonar_range_mm = int(beaper.sonar_distance_cm()*10)
    sonar_time_us = time.ticks_diff(time.ticks_us(), sonar_start)
    
    # Measure time to get ToF range
    tof_start = time.ticks_us()
    tof.start_range_request()
    while not tof.reading_available():
        pass
    tof_range_mm = tof.get_range_value()-30
    tof_time_us = time.ticks_diff(time.ticks_us(), tof_start)
    
    # Write ranges and ranging times into LCD framebuffer
    text = f"D: {tof_range_mm}mm  "
    lcd.write(text, 0, 24, rs24, lcd.WHITE, lcd.BLACK)
    text = f"T: {tof_time_us}us  "
    lcd.write(text, 0, 48, rs24, lcd.WHITE, lcd.BLACK)
    
    text = f"D: {sonar_range_mm}mm  "
    lcd.write(text, 120, 24, rs24, lcd.WHITE, lcd.BLACK)
    text = f"T: {sonar_time_us}us  "
    lcd.write(text, 120, 48, rs24, lcd.WHITE, lcd.BLACK)
    
    # Update LCD from framebuffer
    lcd.update()
