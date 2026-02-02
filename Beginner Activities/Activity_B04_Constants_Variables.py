"""
================================================================================
Beginner Activity 4: Constants and Variables [Activity_B04_Constants_Variables.py]
February 2, 2026

Platform: mirobo.tech BEAPER Pico circuit (any configuration)
Requires: BEAPER_Pico.py board module file
================================================================================
"""
# IMPORTANT: Copy BEAPER_Pico.py into your Raspberry Pi Pico.
import BEAPER_Pico as beaper  # Set up BEAPER Pico I/O

import time

# --- Program Constants ----------------
BLINK_DELAY = 200

# --- Program Variables ----------------
display_pattern = False

beaper.pico_led_on()

while True:
    # Check button state
    if beaper.SW5_pressed():
        display_pattern = True
        
    # LED pattern
    if display_pattern:
        beaper.LED2.value(1)
        time.sleep_ms(BLINK_DELAY)
        beaper.LED3.value(1)
        time.sleep_ms(BLINK_DELAY)
        beaper.LED4.value(1)
        time.sleep_ms(BLINK_DELAY)
        beaper.LED5.value(1)
        time.sleep_ms(BLINK_DELAY)
        beaper.LED2.value(0)
        time.sleep_ms(BLINK_DELAY)
        beaper.LED3.value(0)
        time.sleep_ms(BLINK_DELAY)
        beaper.LED4.value(0)
        time.sleep_ms(BLINK_DELAY)
        beaper.LED5.value(0)
        time.sleep_ms(BLINK_DELAY)
        display_pattern = False
    
    
"""
Program Analysis Activities

1.  


Programming Activities

1.  

"""