"""
Project:  Introductory Programming Activity 5 - Analog
Activity: mirobo.tech/micropython/intro-5-analog
Updated:  July 15, 2025

This introductory programming activity for the mirobo.tech BEAPER Pico
circuit demonstrates analog-to-digital (A-D) conversion and introduces
the print() function for interactive debugging.

Additional program analysis and programming activities demonstrate
f-string formatting in print statements and introduce an Arduino-like
map() function to convert values between different numeric ranges.

See the https://mirobo.tech/beaper webpage for additional BEAPER Pico
programming activities and starter progams.
"""

# Import Pin and time functions
from machine import Pin, PWM, ADC
import time

# Configure Raspberry Pi Pico built-in LED
LED = Pin("LED", Pin.OUT, value=1)

# Configure BEAPER Pico Educational Starter I/O devices
SW2 = Pin(0, Pin.IN, Pin.PULL_UP)
SW3 = Pin(1, Pin.IN, Pin.PULL_UP)
SW4 = Pin(2, Pin.IN, Pin.PULL_UP)
SW5 = Pin(3, Pin.IN, Pin.PULL_UP)
LED2 = M1A = Pin(10, Pin.OUT)
LED3 = M1B = Pin(11, Pin.OUT)
LED4 = M2A = Pin(12, Pin.OUT)
LED5 = M2B = Pin(13, Pin.OUT)
BEEPER = H8OUT = PWM(Pin(14), freq=1000, duty_u16=0)

# Configure analog input devices
Q1 = Q4 = ADC(Pin(26))
Q2 = RV1 = ADC(Pin(27))
Q3 = RV2 = ADC(Pin(28))
VSYS = ADC(Pin(29)) # Pico module system voltage
VTEMP = ADC(ADC.CORE_TEMP) # On-die temperature sensor

while True:
    print()
    
    # On-die temperature sensor
    temp_level = VTEMP.read_u16()
    print("Temperature level:", temp_level)
    
    """
    # Robot floor/line sensor phototransistors
    Q1_level = Q1.read_u16()
    Q2_level = Q2.read_u16()
    Q3_level = Q3.read_u16()
    print("Q1 level:", Q1_level)
    print("Q2 level:", Q2_level)
    print("Q3 level:", Q3_level)
    """
    
    """
    # On-board ambient light sensor
    ambient_light_level = Q4.read_u16()
    print("Light level:", ambient_light_level)
    """
    
    """
    # On-board potentiometers
    RV1_pos = RV1.read_u16()
    RV2_pos = RV2.read_u16()
    print("RV1 position:", RV1_pos)
    print("RV2 position:", RV2_pos)
    """
    
    time.sleep(1)
    

"""
Learn More -- Program Analysis Activities

1.  Let's learn how to read and process analog inputs and print the
    resulting values to the shell in the Python IDE. Unlike digital
    data represented by either 0 or 1, analog data is represented by
    a larger set of values corresponding to voltages between 0V and
    the microcontroller's power supply potentential -- 3.3V in the
    case of the Raspberry Pi Pico. The 12-bit ADC (analog-to-digital
    converter) built into the Raspberry Pi Pico's microcontroller
    physically divides this 3.3V range into 4096 levels, but
    MicroPython typically represents analog input and output values
    using 16-bit numeric values ranging from 0 to 65535.
    
    MicroPython allows programs to run in a REPL (Read, Evaluate,
    Print, Loop) and the microcontroller's USB connection enables
    data to be sent to the terminal or shell in the IDE. No special
    code or configuration is needed to do this -- all that is
    needed is the print() function to display text strings and
    numeric data directly in the IDE.
    
    The Raspberry Pi Pico's microcontroller has five analog input
    channels -- two are connected to internal circuits, and the other
    three can connect to external I/O devices. On BEAPER Pico, the
    three Analog Sensor Select jumpers (JP1, JP2, and JP3) allow
    users to choose between six possible analog input circuits:
    three 'Enviro' (environmental) inputs consisting of ambient
    light sensor Q4 and potentiometers RV1 and RV2, or three 'Robot'
    inputs comprising the optical floor and line sensor module
    phototransistors Q1, Q2, and Q3. Each of these six analog input
    devices can only be used if their related circuit components
    have been installed in the BEAPER Pico circuit board.
    
    The two analog inputs built into the Raspberry Pi Pico module
    itself can be used even if the BEAPER Pico circuit board has
    no analog input circuit components installed. One of these
    measures the microcontroller's power supply input voltage, and
    the other measures the microcontroller's die temperature. Both
    of these inputs are permanently connected and can't be changed,
    so they will be active in every build configuration of BEAPER
    Pico.
    
    If your BEAPER Pico has one or more of the optional analog
    components installed, un-comment the relevant sections of the
    program code to see the readings from the other installed analog
    input devices.
        
    Connect your BEAPER Pico in the IDE and run this program. It
    will read and display a value representing the temperature (as
    well as the values of any other analog inputs you have un-
    commented in the program) once every second. Record the
    temperature value. Does it change over time? How does it change
    if you touch and hold your finger on the microcontroller?
    
2.  The ADC in the Raspberry Pi Pico quantizes input voltages between
    0V and 3.3V into 4096 levels (12-bit binary equivalent values).
    The sensitivity of an ADC circuit can be expressed as the amount
    of input potential corresponding to a single bit change in the
    output. Since the input voltage range and the number of states is
    known, calculate the ADC sensitivity, in mV/bit, by dividing the
    input voltage by the number of states. This will let you know the
    smallest input voltage change that the ADC is able to measure.

3.  MicroPython represents analog values using 16-bit numbers -- with
    65536 states -- even though the ADC only has 12-bit resolution
    (its 12-bit values are simply mapped into a 16-bit numeric range).
    Calculate the sensitivity that an actual 16-bit ADC would have
    over the 0V - 3.3V input range. How much more sensitive would a
    16-bit ADC be than the 12-bit ADC built into the Raspberry Pi
    Pico?
    
    Let's test this to verify the actual analog sensitivity. Run the
    program and alternately warm and cool the temperature sensor by
    touching and removing your finger from the microcontroller. As
    you do so, record the amount that the temperature level changes
    between steps. Does it change by one digit, or a higher amount?
    How does the difference between levels compare to the difference
    between the real (12-bit) and virtual (16-bit) ADC sensitivities
    calculated previously?

    Since analog inputs are translated into 16-bit values, knowing the
    16-bit voltage sensitivity will be important for converting analog
    levels to their equivalent voltages. Add the voltage conversion
    factor calculation into your program (place it above the main
    while loop):

# Pre-calculate ADC voltage conversion factor
ADC_conv_factor = 3.3 / 65535

    Whenever an analog voltage needs to be calculated, it can now
    simply be found by multiplying the analog input level and the
    ADC conversion factor.

4.  The analog temperature sensor built into the Pico microcontroller's
    die has a known voltage offset and temperature coefficient. This
    means that the temperature can be calculated if the voltage across
    the temperature sensor is known. The coversion factor, above, can
    be used to calculate the sensor's voltage. Add the following code
    into the program's while loop to convert the voltage into the
    temperature:

    # The temperature sensor measures the Vbe voltage of a biased bipolar diode, connected to
    # the fifth ADC channel. Typically, Vbe = 0.706V at 27 degrees C, with a slope of -1.721mV
    # (0.001721) per degree.
    temp_volts = temp_level * ADC_conv_factor
    temperature = 27 - (temp_volts - 0.706) / 0.001721
    print("Temp sensor voltage:", temp_volts, "Die temperature:", temperature, "°C")

    This description and the temperature conversion code are based on
    the example in the Raspberry Pi Pico datasheet and show how to
    convert the temperature sensor's voltage into temperature. The
    first line of the program code uses the conversion factor added
    in the step above to convert the temperature sensor value into a
    voltage, and the second line subtracts the temperature calibration
    voltage offset and correlates the sensor diode's temperature
    coefficient with the measured voltage to derive the current die
    temperature. 
    
    Run the program and observe the voltage output and temperature
    output over time. Touch the microcontroller to change the die
    temperature, and once it changes record how much the sensor voltage
    changes by. How does this value relate to the ADC sensitivity
    value calculated earlier?
    
5.  An example temperature sensor voltage reading of 0.7155917 V seems
    to be an extremely precise number, but our previous sensitivity
    calculations reveal that this level of accuracy is higher than the
    actual voltage resolution the ADC is capable of providing. The
    extra digits in the voltage display are simply artifacts of the
    voltage calculation, and do not carry usefully meaningful
    information.
    
    Fortunately, MicroPython includes an f-string formatting method
    that enables long results like this to be rounded down to fewer
    digits, leading to simpler and potentially more realistic
    results. Add the following lines below the existing temperature
    print statement:

    txt = f"Temp sensor voltage: {temp_volts:.4f}V. Die temperature: {temperature:.1f}°C"
    print(txt)

    Run the program again and notice that its new voltage output is
    limited to 4 digits after the decimal point, and the temperature
    output is limited to one digit after the decimal point. Also
    notice that, in comparison with the line above, the 'V' and '°C'
    units are now directly adjacent to their numeric values. Let's
    look at the 'txt' string variable to determine how f-string
    formatting produced this result.
    
    The f-string is a text string (human-readable characters enclosed
    within double-quote marks - " ") preceded by the letter 'f', and
    in this case the text string includes two brace placeholders
    (the parts enclosed within braces - {}). Each brace placeholder
    contains the name of a variable that will be printed followed by
    a colon ':' separator, and one or more formatting options that
    describe how the variable should be interpreted.
    
    In the case of the formatting options used in this code, the
    period represents the numeric decimal point, 4 (and 1) represent
    the number of digits to be displayed following the decimal point,
    and the letter 'f' represents fixed point notation, or a numeric
    format that 'fixes' the length of the number to match the number
    of digits supplied. (f-string formatting can apply to variables,
    expressions, and even functions, and has lots of other formatting
    options available -- see this guide for more information:
    https://www.w3schools.com/python/python_string_formatting.asp)
    
    Adjust the f-string to display the voltage using 3 digits after
    the decimal, and the temperature using two digits after the
    decimal point. Are these values within the measurement precision
    of the 12-bit ADC in the microcontroller?
    
6.  In addition to the on-die temperature sensor, the Raspberry Pi
    Pico's other internally-connected ADC input reads the voltage
    input to its voltage regulator named VSYS (main system voltage)
    through a divide by 3 resistor voltage divider circuit.
    
    The ability for a microcontroller to measure its system voltage
    is useful for battery-operated devices, since it allows them to
    monitor their input voltage and shut down safely, or initiate
    charging, if the battery level drops too low. Add the following
    code to your program to measure the VSYS input voltage (and also
    to approximate the USB VBUS input voltage):

    # VBUS is fed through a series protection diode and into a /3 voltage
    # divider to the VSYS input on the Raspberry Pi Pico. Multiply VSYS by
    # three to restore its potential. Add the diode drop to calculate VBUS. 
    vsys_volts = VSYS.read_u16() * ADC_conv_factor * 3    
    vbus_volts = vsys_volts + 0.275 # At 100mA load current
    txt = f"VSys: {vsys_volts:.2f}V  VBus: {vbus_volts:.2f}V"
    print(txt)

    Here, the ADC reading is coverted to voltage using the same
    conversion factor from step 3, above, and that value is then
    multiplied by 3 to un-do the effect of the voltage divider. The
    VBUS value is calculated by adding the diode voltage drop (a
    value that changes slightly with load current - adjust it as
    necessary based on your circuit).
    
    If you have access to a multimeter, carefully measure the
    VSYS and VBUS voltages on your Raspberry Pi Pico, and adjust
    the VSYS and VBUS calculations to match your measured results.
    
7.  As both of these temperature and voltage conversions have
    demonstrated, converting a value from one numeric range to
    another is a fairly common occurance in analog programs. Let's
    make it easier for you to perform future numeric conversions
    by adding a map() function to your program! Add the function,
    below, into your program above the main while loop:

# Maps a value within the input range to its equivalent in the output range.
def map(value, in_min, in_max, out_min, out_max):
    return(value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    Then, add the following code to test the map() function into
    the main loop of your program:

    print()
    for i in range(0, 65536, 1024):
        txt = f"Input: {i} ==> Output: {map(i, 0, 65535, 0, 100):.2f}%"
        print(txt)
    time.sleep(60)

    The function call 'map(i, 0, 65535, 0, 100)' demonstrates the
    process of converting a 16-bit number, representing an ADC
    result, into an equivalent percentage value. The variable 'i'
    is the input value to be converted by the map() function, and
    in this example is supplied by the for loop instead of being
    an actual ADC result. The input value is followed by the
    lower and upper bounds of its current range -- in this case
    '0' and '65535' corresponding to the minimum and maximum
    16-bit numeric values. Finally, '0' and '100' set the lower
    and upper bound of the new range that the input variable 'i'
    will be mapped into. Run the program to see the output.
    
    Notice that since the map() function itself returns a number,
    the function can be substituted for a numeric variable in
    the f-string, and the f-string will happily format the
    the output of the function!
    

Programming Activities

1.  Create a program that reads the analog value of potentiometer
    RV1 and converts its output to a value that ranges from 0-10
    using the map() function. Convert the mapped value into an
    integer and print it to the shell in your Python IDE using
    f-string formatting.
    
    Try the program in your BEAPER Pico and use RV1 (if it's
    installed, or any of the other analog input devices if RV1
    is not installed) as the input. If no analog devices are
    installed in your BEAPER Pico, simulate the 16-bit analog
    input using values from a for loop as shown above.

2.  Some analog input devices only need to have their values
    monitored to ensure that they remain above or below a specific
    threshold value (or within a certain range), rather than
    having their data continuously processing and converted for
    use. An exammple of this would include using BEAPER Pico's
    optical floor and line sensor modules to detect significant
    differences between light and dark surfaces so that they
    could provide a simple Boolean result to the program.
    
    Create two new program functions, one each for the left and
    right floor (or line) sensors, that will return a Boolean
    state representing the amount of light reflected from the
    floor and into the sensor module's phototransistor.
    
    For example, a function that uses the presence of a line to
    make a decision in a line-following robot could be invoked
    using a function call named like the one in this if condition:

    if left_sees_line():
    
    Determine whether the optiocal sensors in your robot's program
    should be configured for line following, detecting the edge of
    an arena or Sumo ring, or even detecting the edge of a table
    top or staircase, and create an appropriate function for each
    sensor to return its results.

3.  The values from analog inputs can often be used to control analog
    output, either directly, or after processing the input value in
    some way. For example, one of BEAPER Pico's potentiometers could
    be used to control a the brightness of LEDs, or the speed of a
    motor, using PWM pulses – and the map() function can be very
    helpful in doing this.

    Create a program that uses the map() function to control the
    speed of ventillation fans in a greenhouse. Imagine that a
    greenhouse owner has installed a temperature sensor and variable
    speed fan in their greenhouse, and would like have the fans
    automatically controlled based on the temperature. When the
    green house temperature reaches 20°C, the fans should run at
    10% speed, ramping up to 100% speed when the temperature is
    at or above 28°C.

4.  Programming activity 2, above, described comparing light levels
    with digital threshold values, and this strategy can be used to
    create a simple line-following robot. Robots controlled this way
    will follow the line with a jerky motion, rapidly changing
    direction to keep their sensors on the line.
    
    Analog input and PWM output can be used to create a robot with
    much smoother response by adjusting its motor speed to more
    rapidly correct for large differences between the left and right
    sensor values, or to adjust the speed in smaller amounts when
    both sensors see nearly identical values.
    
    Plan, implement, and test an analog-based control program for a
    line-following robot. You will also need to consider what happens
    when neither line sensor detects the line, and you might need to
    implement some sort of sensor calibration if the left and right
    line sensor phototransistors produce significantly different
    results while observing the line or floor.

"""