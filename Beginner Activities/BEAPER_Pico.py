"""
BEAPER_Pico.py
March 14, 2026

Board support module for the mirobo.tech BEAPER Pico circuit.

This module configures Raspberry Pi Pico's GPIO pins for BEAPER
Pico's on-board circuits and provides simple helper functions to
enable beginners to focus on learning programming concepts first.

Before getting started with it you should know:
- nothing here is hidden, or * magic *, or requires special libraries
- the functions are just normal Python code to help you start learning
- you're encouraged to modify the code to make it work better for you!

BEAPER Pico hardware notes:
- Buttons use internal pull-up resistors (so pressed == 0)
- LEDs and motor driver share I/O pins (so much I/O, too few I/O pins!)
- Analog jumpers on BEAPER Pico must be set to connect sensors to pins:
    - Enviro. position selects light sensor Q4, and pots RV1 and RV2
    - Robot position selects floor/line phototransistors Q1, Q2, and Q3
"""

import machine
from machine import Pin, ADC, PWM, I2C
import time

# ---------------------------------------------------------------------
# Raspberry Pi Pico Module LED
# ---------------------------------------------------------------------

PICO_LED = Pin("LED", Pin.OUT)

def pico_led_on():
    # Turn the Raspberry Pi Pico on-board LED on.
    PICO_LED.value(1)

def pico_led_off():
    # Turn the Raspberry Pi Pico on-board LED off.
    PICO_LED.value(0)

def pico_led_toggle():
    # Toggle the Raspberry Pi Pico on-board LED.
    PICO_LED.value(not PICO_LED.value())


# ---------------------------------------------------------------------
# BEAPER Pico LEDS
# ---------------------------------------------------------------------

# IMPORTANT: LED pins are shared with the motor controller. Using the
# LEDs while the the motors are active will affect motor behavior!

LED2_PIN = const(10)  # Motor 1A (Motor 1 = left motor)
LED3_PIN = const(11)  # Motor 1B
LED4_PIN = const(12)  # Motor 2A (Motor 2 = right motor)
LED5_PIN = const(13)  # Motor 2B

LED2 = Pin(LED2_PIN, Pin.OUT)
LED3 = Pin(LED3_PIN, Pin.OUT)
LED4 = Pin(LED4_PIN, Pin.OUT)
LED5 = Pin(LED5_PIN, Pin.OUT)

LEDS = (LED2, LED3, LED4, LED5)  # Tuple of all LED pins
# Useful for iterating through all LEDS - see below:

def leds_on():
    # Turn all four LEDs on
    for led in LEDS:
        led.value(1)
        
def leds_off():
    # Turn all four LEDs off
    for led in LEDS:
        led.value(0)


# ---------------------------------------------------------------------
# BEAPER Pico Pushbutton Switches
# ---------------------------------------------------------------------

# All pushbutton switches use internal pull-up resistors (active LOW)

SW2_PIN = const(0)  # SW2
SW3_PIN = const(1)  # SW3
SW4_PIN = const(2)  # SW4
SW5_PIN = const(3)  # SW5
# Note: const() stores fixed values in ROM to save RAM

SW2 = Pin(SW2_PIN, Pin.IN, Pin.PULL_UP)
SW3 = Pin(SW3_PIN, Pin.IN, Pin.PULL_UP)
SW4 = Pin(SW4_PIN, Pin.IN, Pin.PULL_UP)
SW5 = Pin(SW5_PIN, Pin.IN, Pin.PULL_UP)

SWITCHES = (SW2, SW3, SW4, SW5)  # Tuple of all pushbutton switch pins
# Useful for iterating through all SWITCHES - see LEDS examples, above.

# ---------------------------------------------------------------------
# BEAPER Pico Motor Controller
# ---------------------------------------------------------------------

# IMPORTANT: Motor controller is connected to LED pins! Using the
# LEDs while the the motors are active will affect motor behavior!

# NOTE: The forward and reverse directions of each motor are dependent
# on both program code and physical motor wiring connections on CON1.

M1A = LED2  # Left motor terminal A
M1B = LED3  # Left motor terminal B
M2A = LED4  # Right motor terminal A
M2B = LED5  # Right motor terminal B

def motors_stop():
    M1A.value(0)
    M1B.value(0)
    M2A.value(0)
    M2B.value(0)

def left_motor_forward():
    M1A.value(1)
    M1B.value(0)

def left_motor_reverse():
    M1A.value(0)
    M1B.value(1)
    
def left_motor_stop():
    M1A.value(0)
    M1B.value(0)

def right_motor_forward():
    M2A.value(0)
    M2B.value(1)  # Opposite of left_motor_forward()

def right_motor_reverse():
    M2A.value(1)  # Opposite of left_motor_reverse()
    M2B.value(0)

def right_motor_stop():
    M2A.value(0)
    M2B.value(0)
    

# ---------------------------------------------------------------------
# BEAPER Pico Piezo Buzzer (BEAPER's beeper!)
# ---------------------------------------------------------------------

# Generate tones using PWM (similar to Arduino tone() functions)

LS1_PIN = const(14)  # Also wired to 5V output header H8

LS1 = PWM(Pin(LS1_PIN))

def tone(frequency, duration=None):
    # Start a tone at specified frequency (Hz), and stop the tone after
    # an optional duration (ms). Adding duration causes a blocking delay.
    LS1.freq(frequency)
    LS1.duty_u16(32768)
    if duration is not None:
        time.sleep_ms(duration)
        noTone()

def noTone(duration=None):
    # Stop the tone. Optionally pause (blocking) for the duration (ms). 
    LS1.duty_u16(0)
    if duration is not None:
        time.sleep_ms(duration)

def beep(duration=100):
    # Play a short beep (100ms by default)
    tone(1000, duration)
    

# ---------------------------------------------------------------------
# BEAPER Pico Analog Inputs and Raspberry Pi Pico Analog sensors
# ---------------------------------------------------------------------

# IMPORTANT: On-board analog jumpers must be used to select analog devices.

ADC0_PIN = const(26)  # Ambient light sensor Q4 OR floor sensor Q1
ADC1_PIN = const(27)  # Pot RV1 OR line sensor Q2
ADC2_PIN = const(28)  # Pot RV2 OR floor/line sensor Q3

# BEAPER Pico analog inputs
ADC0 = ADC(Pin(ADC0_PIN))
ADC1 = ADC(Pin(ADC1_PIN))
ADC2 = ADC(Pin(ADC2_PIN))

def light_level():
    # Read Q4 ambient light sensor value. Set JP1 to Enviro.
    return 65535-ADC0.read_u16()  # Brighter -> higher values

def Q1_level():
    # Read floor sensor Q1. Set JP1 to Robot.
    return 65535-ADC0.read_u16()  # Higher reflectivity -> higher values

def Q2_level():
    # Read line sensor Q2. Set JP2 to Robot.
    return 65535-ADC1.read_u16()  # Higher reflectivity -> higher values

def Q3_level():
    # Read floor/line sensor Q3. Set JP3 to Robot.
    return 65535-ADC2.read_u16()  # Higher reflectivity -> higher values

def RV1_level():
    # Read potentiometer RV1. Set JP2 to Enviro.
    return ADC1.read_u16()  # Clockwise -> higher values

def RV2_level():
    # Read potentiometer RV2. Set JP3 to Enviro.
    return ADC2.read_u16()  # Clockwise -> higher values

# Raspberry Pi Pico VSYS input
VSYS = ADC(Pin(29))  # Regulator input voltage VSYS / 3

def VSYS_volts():
    # Read system voltage in volts.
    return VSYS.read_u16() * 9.9 / 65535

# RP2xxxx die temperator sensor input
MCU_TEMP = ADC(ADC.CORE_TEMP)

def mcu_temperature():
    # Read MCU die temp in degrees C. From the Raspberry Pi Pico datasheet:
    # The temperature sensor measures the Vbe voltage of a biased bipolar
    # diode, connected to the fifth ADC channel. Typically, Vbe = 0.706V
    # at 27 degrees C, with a slope of -1.721mV (0.001721) per degree.
    mcu_temp_volts = MCU_TEMP.read_u16() * 3.3 / 65535
    return 27 - (mcu_temp_volts - 0.706) / 0.001721


# ---------------------------------------------------------------------
# QWIIC/I2C Connector J4 (supports 3.3V I2C devices)
# ---------------------------------------------------------------------

I2C_ID = 0
SDA = Pin(4)
SCL = Pin(5)
QWIIC = I2C(id=I2C_ID, sda=SDA, scl=SCL)


# ---------------------------------------------------------------------
# 3.3V Digital I/O Headers H1-H4 (supports 3.3V HC-SR04P SONAR module)
# ---------------------------------------------------------------------

# 3.3V digital I/O header (optional SONAR module shares H2 and H3)

H1_PIN = const(6)   # H1
H2_PIN = const(7)   # H2 (SONAR TRIG)
H3_PIN = const(8)   # H3 (SONAR ECHO)
H4_PIN = const(9)   # H4

# Ultrasonic SONAR distance measurement function. Returns the distance
# to the nearest target within max_range in cm (defaults to 1m).

SONAR_TRIG = Pin(H2_PIN, Pin.OUT, value=0)
SONAR_ECHO = Pin(H3_PIN, Pin.IN)

def sonar_range(_max_range=100):
    # Returns either:
    #  distance (cm) - closest target within _max_range
    #  0             - no target detected within _max_range
    #  -1            - time-out waiting for ECHO to start
    #  -2            - previous ECHO is still in progress

    # Return -2 if a previous ECHO pulse is still in progress
    if SONAR_ECHO.value() == 1:
        return -2   # (wait 10ms after ECHO ends before re-triggering)
  
    # Make a 10us TRIG pulse to start a range measurement
    SONAR_TRIG.value(1)
    time.sleep_us(10)
    SONAR_TRIG.value(0)

    # Wait up to 2500us for ECHO pin to go high after TRIG.
    # (Necessary for 3.3V HC-SR04P/RCWL-9610A SONAR modules.)
    duration = machine.time_pulse_us(SONAR_ECHO, 0, 2500)
    # time_pulse_us returns -2 if ECHO pin never goes low or -1 if
    # ECHO is low for > 2500us. Either way, ECHO did not start.
    if duration < 0:
        return -1

  # Measure ECHO pulse duration. Time-out value is set to round-trip
  # time for max_range plus 1cm, in microseconds. (~29us/cm one way)
    duration = machine.time_pulse_us(SONAR_ECHO, 1, (_max_range + 1) * 58)
    
    # time_pulse_us returns -1 if ECHO times out (no target within _max_range)
    if duration < 0:
        return 0

    # Convert round trip ECHO time to distance
    return int(duration / 58)


# ---------------------------------------------------------------------
# 5V Digital Output Headers H5-H8 (supports 3 servos)
# ---------------------------------------------------------------------

# 5V Digital output headers (output only)
H5_PIN = const(20)  # Servo 1
H6_PIN = const(21)  # Servo 2
H7_PIN = const(22)  # Servo 3
H8_PIN = LS1_PIN    # Same as piezo speaker pin

# Servo pulse width constants (microseconds). Adjust for your servo.
# Standard 90-degree servo: 1000us to 2000us
SERVO_MIN_US = const(1000)   # Pulse width at 0 degrees
SERVO_MAX_US = const(2000)   # Pulse width at maximum angle
SERVO_RANGE  = const(90)     # Maximum servo angle (degrees)

# Servos are initialized to centre position (duty_u16=4915 ≈ 1.5ms).
# This value is calculated from: 
#   - pulse period: 1 / 50Hz pulse frequency = 20ms period
#   - 1.5ms pulse: duty_u16 = (1.5 / 20.0) * 65535 = 4915
# Modify the duty_u16 value if the centre position is not safe for
# your application before connecting servos to the circuit.
SERVO1 = PWM(Pin(H5_PIN), freq=50, duty_u16=4915)
SERVO2 = PWM(Pin(H6_PIN), freq=50, duty_u16=4915)
SERVO3 = PWM(Pin(H7_PIN), freq=50, duty_u16=4915)

SERVOS = (SERVO1, SERVO2, SERVO3)  # Tuple of all servo PWM outputs

def set_servo(servo, angle):
    # Set a servo to angle (0 to SERVO_RANGE degrees).
    # Pass the servo object as the first argument: set_servo(SERVO1, 45)
    angle = max(0, min(SERVO_RANGE, angle))
    pulse_us = SERVO_MIN_US + int(angle / SERVO_RANGE * (SERVO_MAX_US - SERVO_MIN_US))
    servo.duty_ns(pulse_us * 1000)
    return angle
  