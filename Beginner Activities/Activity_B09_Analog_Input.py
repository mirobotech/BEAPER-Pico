"""
================================================================================
Beginner Activity 9: Analog Input [Activity_B09_Analog_Input.py]
February 28, 2026

Platform: mirobo.tech BEAPER Pico circuit (any configuration)
Requires: BEAPER_Pico.py board module file.

Analog jumper settings for this activity:
  JP1 - Enviro. (selects ambient light sensor Q4)
  JP2 - Enviro. (selects potentiometer RV1)
  JP3 - Enviro. (selects potentiometer RV2)
================================================================================
"""
# IMPORTANT: Copy BEAPER_Pico.py into your Raspberry Pi Pico
import BEAPER_Pico as beaper  # Set up BEAPER Pico I/O

import time

# --- Program Constants ----------------
STEP_DELAY = const(100)               # Main loop delay (ms)
LIGHT_HIGH = const(45000)             # Light threshold: LED turns on above this
LIGHT_LOW  = const(35000)             # Light threshold: LED turns off below this
TONE_MIN   = const(200)               # Minimum theremin frequency (Hz)
TONE_MAX   = const(4000)              # Maximum theremin frequency (Hz)

# --- Program Variables ----------------
light_on = False                      # Hysteresis state for light threshold


# --- Program Functions ----------------

def map_range(value, in_min, in_max, out_min, out_max):
    # Map a value from one range to another, returning a float result.
    # Use int(map_range(...)) when an integer result is required.
    return out_min + (value - in_min) * (out_max - out_min) / (in_max - in_min)

def show_bar(level, max_level):
    # Display a bar graph on LEDs 2-5 proportional to level out of max_level.
    # Thresholds are centred in each quarter so all LEDs can light fully.
    beaper.LED2.value(level > max_level * 1 // 8)
    beaper.LED3.value(level > max_level * 3 // 8)
    beaper.LED4.value(level > max_level * 5 // 8)
    beaper.LED5.value(level > max_level * 7 // 8)


# --- Main Program ---------------------

beaper.pico_led_on()
print("Activity 9: Analog Input")
print("JP1=Enviro, JP2=Enviro, JP3=Enviro")
print()

while True:
    # Part 1: Read potentiometer RV1 and display as bar graph and raw value
    rv1 = beaper.RV1_level()
    show_bar(rv1, 65535)
    print("RV1:", rv1, end="  ")

    # Part 2: Read potentiometer RV2 and use it to control the tone frequency
    rv2 = beaper.RV2_level()
    frequency = int(map_range(rv2, 0, 65535, TONE_MIN, TONE_MAX))
    beaper.tone(frequency)
    print("RV2:", rv2, "Freq:", frequency, "Hz", end="  ")

    # Part 3: Read sensors and convert to meaningful units
    light = beaper.light_level()
    temp = beaper.mcu_temperature()
    vsys = beaper.VSYS_volts()
    print("Light:", light, "Temp:", round(temp, 1), "C",
          "Vsys:", round(vsys, 2), "V", end="  ")

    # Part 4: Threshold detection with hysteresis on light sensor
    if light_on:
        if light < LIGHT_LOW:
            light_on = False
            beaper.pico_led_off()
    else:
        if light > LIGHT_HIGH:
            light_on = True
            beaper.pico_led_on()

    print("Light LED:", light_on)
    time.sleep_ms(STEP_DELAY)


"""
Guided Exploration

All of the programs so far have used digital I/O - inputs and outputs
that are either fully on or fully off. The real world is rarely that
simple: temperature, light, sound, and position all vary continuously
across a range of values. Microcontrollers read these continuously
varying physical quantities using an Analog to Digital Converter, or
ADC, which turns a voltage into a number the program can work with.
The two functions in this program apply the patterns from Activity 8
- parameters, return values, and encapsulation - to sensor data,
converting raw ADC readings into bar graph displays and musical tones.
This activity also works with integer and float numeric types in detail
- the Numeric Types sidebar is a useful reference if you want to
review how these types work.

1.  The Raspberry Pi Pico's ADC returns values from 0 to 65535 -
    a 16-bit range. This means the ADC divides the full input
    voltage range (0 to 3.3V) into 65536 steps, giving a resolution
    of about 0.05mV per step.

    The board module's analog helper functions return these raw
    ADC values directly. When you turn RV1 fully anti-clockwise,
    'RV1_level()' returns approximately 0. Fully clockwise returns
    approximately 65535. Observe the console while slowly rotating
    RV1 from one extreme to the other. Is the change perfectly
    smooth, or do you notice any irregularities?

    Why do you think the ADC uses a range of 0-65535 specifically,
    rather than 0-100 or 0-1000? Think about how 65536 relates to
    powers of 2 and the binary number system from Activity 7. The
    Numeric Types sidebar explains why integer sizes are always
    powers of 2.

2.  The 'map_range()' function converts a value from one numeric
    range to another:

    def map_range(value, in_min, in_max, out_min, out_max):
        return out_min + (value - in_min) * (out_max - out_min) / (in_max - in_min)

    Trace through this formula with value=32767 (approximately
    halfway), in_min=0, in_max=65535, out_min=200, out_max=4000.
    What frequency would this produce? Does it match what you
    would expect for a value halfway through the input range?

    Notice that the function uses '/' rather than '//'. This means
    it returns a float - a number with a decimal point. The main
    loop wraps the result in 'int()' before passing it to 'tone()':

    frequency = int(map_range(rv2, 0, 65535, TONE_MIN, TONE_MAX))

    Why is the 'int()' conversion necessary here? In Activity 8
    GE8 you discovered that 'beaper.tone()' behaves differently
    with a float argument than with an integer. Try removing the
    'int()' conversion and observe what happens - does the result
    match what you would predict?

3.  The 'show_bar()' function divides the LED range into four
    bands, with thresholds centred in each quarter:

    beaper.LED2.value(level > max_level * 1 // 8)
    beaper.LED3.value(level > max_level * 3 // 8)
    beaper.LED4.value(level > max_level * 5 // 8)
    beaper.LED5.value(level > max_level * 7 // 8)

    The thresholds are at 1/8, 3/8, 5/8, and 7/8 of max_level -
    the midpoints of each quarter. This means each LED represents
    one quarter of the input range, and all four LEDs can light
    when the value is high enough.

    Trace through the function with max_level=65535 and these
    values of level: 0, 8192, 24576, 40960, 57344, 65535.
    Which LEDs are lit for each value?

    The '//' operator is integer division - it divides and discards
    any remainder, always returning a whole number. This is the
    opposite of '/' which, as you will explore in GE5, always
    returns a float. Using '//' here keeps the threshold
    calculations as integers, which is appropriate since LED pin
    values and ADC counts are always whole numbers.

    Notice the operator precedence: 'max_level * 1 // 8' is
    evaluated as '(max_level * 1) // 8' rather than
    'max_level * (1 // 8)'. Try evaluating '1 // 8' on its own
    in the console. What result do you get, and what would happen
    to 'show_bar()' if the division were performed first?

    Compare 'show_bar()' with 'indicate_attempts()' from
    Activity 8. Both display a level on four LEDs, but
    'show_bar()' works with any maximum value, not just 4.
    What did making the function more general require, and what
    did it make possible?

4.  Part 2 maps RV2 to a tone frequency, creating a theremin-like
    instrument. The tone plays continuously because 'beaper.tone()'
    is called without a duration argument - it starts the tone and
    returns immediately, leaving the tone running until something
    stops it.

    Open BEAPER_Pico.py and re-read the 'tone()' and 'noTone()'
    functions you examined in Activity 8. Under what conditions
    does 'tone()' call 'noTone()' automatically? If 'tone()' is
    called without a duration, what is the only way to stop the
    tone?

    The function 'read_keypad()' from Activity 8 is not suitable
    for use inside a loop that needs to keep updating sensor
    readings and tone frequency. What property of 'read_keypad()'
    would cause problems here? Think about what the function does
    while it is waiting for a button press.

    Modify the main loop to silence the tone while SW5 is held
    down, using 'beaper.SW5.value() == 0' as the check and
    'beaper.noTone()' to stop the sound. The tone should resume
    automatically on the next iteration when SW5 is released.

5.  The MicroPython console is more than just a place to see
    output from 'print()' - it is a live interpreter that evaluates
    any MicroPython expression you type directly. This makes it a
    powerful tool for exploring how the language works.

    Stop the running program by pressing Ctrl-C. The console will
    show a '>>>' prompt, indicating that it is ready to accept
    expressions directly. Type each of the following one at a time
    and press Enter after each. Record what you see:

    10 / 2
    10 // 2
    print(10 / 2)
    print(10 // 2)
    print(type(10 / 2))
    print(type(10 // 2))
    print(type(200))
    print(type(3.3))
    x = 65535
    print(x * 3.3 / 65535)
    print(type(x * 3.3 / 65535))

    MicroPython has two main numeric types: 'int' (whole numbers)
    and 'float' (numbers with a decimal point). The '/' operator
    always produces a float, even when the result is a whole
    number. The '//' operator always produces an int, discarding
    any remainder.

    This matters for hardware functions. Using the console, try:

    import BEAPER_Pico as beaper
    beaper.tone(1000)
    beaper.tone(1000.0)

    What difference do you observe? This is why 'map_range()'
    returns a float but the main loop converts it to int before
    passing it to 'beaper.tone()'.

    When you are finished exploring, press Ctrl-D or reset the
    board to restart the program.

6.  Part 3 reads the Raspberry Pi Pico's on-die temperature sensor
    and system supply voltage using two board module functions:

    temp = beaper.temp_C()
    vsys = beaper.Vsys_Volts()

    Open BEAPER_Pico.py and find the definitions of 'temp_C()'
    and 'Vsys_Volts()'. Each performs a two-step conversion: first
    turning the raw ADC value into a voltage, then converting that
    voltage into a meaningful physical quantity.

    For 'temp_C()': why is the raw ADC value multiplied by 3.3
    and divided by 65535 as the first step? The second step uses
    the formula '27 - (die_temp_volts - 0.706) / 0.001721', where
    the constants 0.716 and 0.001721 describe the specific
    characteristics of the Pico's on-die sensor as documented in
    the Raspberry Pi Pico datasheet. What does subtracting from 27
    accomplish, and what does dividing by 0.001721 represent
    physically?

    For 'Vsys_Volts()': the raw reading is multiplied by 9.9
    rather than 3.3. Why 9.9? The Pico's VSYS pin is connected
    to a voltage divider that reduces the supply voltage to a
    safe ADC input level. What division ratio does the factor
    9.9 imply, and why is knowing the supply voltage useful for
    a battery-powered robot?

    The on-die temperature measures the Pico chip's internal
    temperature. Would you expect it to read higher or lower than
    the room temperature, and why? Run the program and observe
    the reading over several minutes - does it match your
    prediction, and what physical process causes any difference
    from ambient temperature?

7.  Before tuning the threshold values for the hysteresis light
    detector that will be created in GE8, below, it helps to know
    the actual range of values the light sensor produces in your
    environment. Hysteresis is a technique that uses two thresholds -
    one to turn something on, and a lower one to turn it off - to
    prevent flickering when a reading hovers near a single boundary.
    GE8 covers this in detail; first, take some measurements to
    calibrate the thresholds to your environment.

    Temporarily add two variables before the main loop to track
    the minimum and maximum light readings seen so far:

    light_min = 65535
    light_max = 0

    Inside the main loop, after reading 'light', add:

    if light < light_min:
        light_min = light
    if light > light_max:
        light_max = light
    print("Min:", light_min, "Max:", light_max)

    Run the program and slowly cover Q4 completely with your
    finger, then uncover it fully and hold it near a bright
    light source. Record the minimum and maximum values you
    observe. These represent the practical range of your sensor
    in its current environment.

    Remove the tracking code once you have your readings. You
    will use these values to set appropriate LIGHT_HIGH and
    LIGHT_LOW thresholds in GE8.

8.  A single threshold would turn the status LED on when light
    exceeds it and off when light falls below it - but when the
    light level hovers near the boundary, the LED flickers
    rapidly as the reading crosses the threshold many times
    per second.

    Hysteresis solves this with two thresholds: the LED turns
    on only when light rises above LIGHT_HIGH, and turns off
    only when it falls below LIGHT_LOW. The gap between them
    creates a band of values where the LED holds its current
    state regardless of small fluctuations.

    The 'light_on' variable is declared before the main loop,
    not inside it. Why is this essential to the hysteresis
    behaviour? What would happen if 'light_on = False' were
    inside the loop?

    Using the minimum and maximum readings from GE7, set
    LIGHT_HIGH to approximately 75% of the way between your
    minimum and maximum, and LIGHT_LOW to approximately 25%.
    Slowly cover and uncover Q4 while watching the status LED.
    Does the LED respond without flickering near the transition?

    Reduce the gap between LIGHT_HIGH and LIGHT_LOW gradually
    until flickering begins. What is the minimum gap that prevents
    flickering under your lighting conditions? What happens if
    you set LIGHT_LOW higher than LIGHT_HIGH?

9.  The main loop prints all sensor readings on a single line
    using 'end=""' to suppress the normal newline after each
    print, with a final newline at the end of the iteration:

    print("RV1:", rv1, end="  ")
    ...
    print("Light LED:", light_on)

    This keeps each loop iteration on one line in the console,
    making it easier to observe all values changing together.

    Add a loop counter variable that increments on each iteration
    and prints at the start of each line (e.g. "1:", "2:"...) to
    make it easier to correlate readings across iterations.

    Observe the rate at which lines appear. What STEP_DELAY value
    gives the best balance between a fast sensor update rate and
    output that is readable? Human perception has a limit of around
    50-100ms - below that threshold, reducing STEP_DELAY further
    will not make the sensor response feel more immediate, but the
    console output will become harder to read.


Extension Activities

These activities build on the sensor-reading and function patterns
from the starter program. Use named constants for all threshold and
scaling values, and named functions for any reusable behaviour.

1.  Modify 'show_bar()' so that it accepts an optional third
    argument 'invert' that defaults to False. When invert is True,
    the bar fills from right to left - LED5 lights first at low
    values, LED2 last at high values. Use this to display the
    light level inverted, so that a darker environment produces
    a fuller bar.

    MicroPython supports default parameter values in functions:

    def show_bar(level, max_level, invert=False):

    Call 'show_bar(light, 65535, invert=True)' for the light
    display and verify it responds correctly. What does this tell
    you about how default parameters make functions more flexible
    without requiring changes to existing calls?

2.  Write a 'temp_trend()' function that compares the current
    temperature with the previous reading and returns the string
    'rising', 'falling', or 'steady'. Store the previous reading
    in a variable declared before the main loop. Print the trend
    alongside the current temperature on each iteration.

    What threshold difference in degrees C makes a useful 'steady'
    band that avoids constant switching due to sensor noise? The
    Pico's on-die temperature sensor measures the chip's internal
    temperature rather than ambient room temperature - how might
    this affect its usefulness for detecting environmental trends,
    and would you expect it to be more or less stable than a
    dedicated ambient temperature sensor?

3.  Create a data logger that records the minimum and maximum
    values seen for RV1, the light level, and temperature since
    the program started. Print the current value, minimum, and
    maximum for each sensor on every iteration. When SW5 is
    pressed, reset all minimums and maximums to their starting
    values.

    Think carefully about initial values: what should the minimum
    start at so that the first real reading always replaces it?
    What should the maximum start at? What happens to your
    approach if the sensor range is not known in advance?

4.  Write a 'calibrate(sensor_fn, samples)' function that calls
    a sensor function 'samples' times with a short delay between
    readings, discards the highest and lowest values, and returns
    the average of the remainder as a float. The first argument
    should be a function - for example, 'beaper.RV1_level' (without
    brackets, so the function itself is passed, not its result).

    Call this function once at startup for RV1 and the light
    sensor, storing the results as baseline values. In the main
    loop, display the difference between the current reading and
    the baseline rather than the raw value.

    Hint: in MicroPython you can pass a function as an argument
    and call it inside the receiving function. Here is the basic
    structure showing how to call the passed-in sensor function
    and accumulate readings - the trimming and averaging logic is
    yours to implement:

    def calibrate(sensor_fn, samples):
        total = 0
        for _ in range(samples):
            total += sensor_fn()      # Call the passed-in function
            time.sleep_ms(10)
        # Add trimming and return the average here

    This technique - averaging after discarding the extremes - is
    called a trimmed mean, and it reduces the effect of occasional
    noisy readings on the result. This is also a preview of
    functions as first-class values - a concept covered in full
    in the intermediate activities.

5.  Build a simple environmental monitor using all available analog
    inputs. Display temperature in degrees C and light as a
    percentage of the calibrated maximum. Use RV1 to set a
    temperature alarm threshold and RV2 to set a light alarm
    threshold. When either sensor exceeds its threshold, sound
    a distinctive alarm tone and flash the corresponding LED.
    Display the Vsys voltage as an additional status indicator.

    Structure the program using functions for each major task:
    reading and converting each sensor, checking each threshold,
    and triggering each alarm. How does organising the program
    this way compare to writing it as a single sequential block?
    What would make it harder to add a third sensor later?

"""
