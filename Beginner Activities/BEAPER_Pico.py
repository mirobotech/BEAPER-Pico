"""
BEAPER_Pico.py
February 18, 2026

Board support module for the mirobo.tech BEAPER Pico circuit.

This module configures Raspberry Pi Pico's GPIO pins for BEAPER
Pico's on-board circuits and provides simple helper functions to
enable beginners to focus on programming concepts first.

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
# BEAPER Pico Pushbutton Switches
# ---------------------------------------------------------------------

# All pushbutton switches use internal pull-up resistors (active LOW)

SW2_PIN = const(0)  # SW2
SW3_PIN = const(1)  # SW3
SW4_PIN = const(2)  # SW4
SW5_PIN = const(3)  # SW5

SW2 = Pin(SW2_PIN, Pin.IN, Pin.PULL_UP)
SW3 = Pin(SW3_PIN, Pin.IN, Pin.PULL_UP)
SW4 = Pin(SW4_PIN, Pin.IN, Pin.PULL_UP)
SW5 = Pin(SW5_PIN, Pin.IN, Pin.PULL_UP)

def SW2_pressed():
    # Return True if pushbutton 2 is pressed.
    return SW2.value() == 0

def SW3_pressed():
    # Return True if pushbutton 3 is pressed.
    return SW3.value() == 0

def SW4_pressed():
    # Return True if pushbutton 4 is pressed.
    return SW4.value() == 0

def SW5_pressed():
    # Return True if pushbutton 5 is pressed.
    return SW5.value() == 0


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

# Generate tones using PWM (simiar to Arduino tone() functions)

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

def Vsys_Volts():
    # Read system voltage in volts.
    return VSYS.read_u16() * 9.9 / 65535

# RP2xxxx die temperator sensor input
DIE_TEMP = ADC(ADC.CORE_TEMP)

def temp_C():
    # Read die temp in degrees C.
    die_temp_volts = DIE_TEMP.read_u16() * 3.3 / 65535
    return 25 - (die_temp_volts - 0.716) / 0.001721


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

# Ultrasonic SONAR distance measurement function

SONAR_TRIG = Pin(H2_PIN, Pin.OUT, value=0)
SONAR_ECHO = Pin(H3_PIN, Pin.IN)

def sonar_distance_cm(max=300):
  # Returns either:
  #  - distance (cm) to the closest target, up to max distance (cm)
  #  - 0 if no target is detected within max distance
  #  - error code (-1, -2) from the time_pulse_us() function
  #  - error code (-3) if a previous ECHO is still in progress

  if SONAR_ECHO.value() == 1:
    # Check if previous ECHO is in progress, return error if so
    return -3   # (wait 10ms after ECHO ends before re-triggering)
  
  # Create a TRIG pulse
  SONAR_TRIG.value(1)
  time.sleep_us(10)
  SONAR_TRIG.value(0)
  
  # Wait 2500us for ECHO pulse to start. Note: HC-SR04P (3.3V-capable
  # modules also labelled as RCWL-9610A 2022) delay for approximately
  # 2300us after the TRIG pulse ends and the ECHO pulse starts.
  
  duration = machine.time_pulse_us(SONAR_ECHO, 0, 2500)

  if duration < 0:
    # ECHO didn't start - return time_pulse_us() error (-2, -1)
    return duration
  
  # Time ECHO pulse. Set time-out value to max range.
  duration = machine.time_pulse_us(SONAR_ECHO, 1, (max + 1) * 58)
  if duration < 0:
    return 0    # Distance > max range
  
  # Calculate target distance in cm
  return duration / 58


# ---------------------------------------------------------------------
# 5V Digital Output Headers H5-H8 (supports 3 servos)
# ---------------------------------------------------------------------

# 5V Digital output headers (output only)
H5_PIN = const(20)  # Servo 1
H6_PIN = const(21)  # Servo 2
H7_PIN = const(22)  # Servo 3
H8_PIN = LS1_PIN    # Same as piezo speaker pin

SERVO1 = PWM(Pin(H5_PIN), freq=50, duty_u16=4916)
SERVO2 = PWM(Pin(H6_PIN), freq=50, duty_u16=4916)
SERVO3 = PWM(Pin(H7_PIN), freq=50, duty_u16=4916)

def SERVO1_angle(angle):
    """
    Set servo 1 to angle (0–90 degrees).
    
    90 degree servo pulses range from 1-2 ms. Servo pulse is created
    using PWM, so pulse length is derived from duty cycle of the frame:
    
    1ms pulse / 20ms frame * 65536 (16-bit PWM range) = 3276.8 (use 3277)
    2ms pulse / 20ms frame * 65536 = 6554
    
    Duty cycles from 3277 to 6554 correspond to 0-90 degrees of motion.
    """
    angle = max(0, min(90, 90-angle))
    duty = int(3277 + (angle / 90) * 3277)
    SERVO1.duty_u16(duty)

def SERVO2_angle(angle):
    angle = max(0, min(90, 90-angle))
    duty = int(3277 + (angle / 90) * 3277)
    SERVO2.duty_u16(duty)

def SERVO3_angle(angle):
    angle = max(0, min(90, 90-angle))
    duty = int(3277 + (angle / 90) * 3277)
    SERVO3.duty_u16(duty)

