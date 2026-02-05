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
BLINK_DELAY = const(200)

# --- Program Variables ----------------
SW2_pressed = False
display_pattern = False

beaper.pico_led_on()

while True:
    SW2_pressed = (beaper.SW2.value() == 0)
    
    # Check button state
    if SW2_pressed:
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

1.  In the input activity:

    beaper.SW2.value() == 0
    
    explain true condition...
    
2.  constants CAPS, variables lower
    
    explain what happens, predict how many times pattern will flash when button
    is pressed

2.  change BLINK_DELAY - easy

3.  convert BLINK_DELAY to variable, set blink delay based on button

4.   


Programming Activities

1.  

"""