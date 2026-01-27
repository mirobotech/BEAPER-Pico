"""
BEAPER Pico I/O Test Project
March 10, 2025

Functional test of all on-board BEAPER Pico I/O devices.

This program includes a SONAR range function designed to test an optional 3.3V
HC-SR04P ultrasonic distance sensor module plugged into headers H1-H4, as well
as servo position functions to control two servos connected to H5 and H6 from
potentiometers RV1 and RV2.

The program displays the SONAR range and analog input values from the ambient
light sensor, temperature sensor, and both on-board potentiometers. Set the
jumpers to select the environmental inputs (labelled Enviro.) on the BEAPER
Pico PCB.

See the https://mirobo.tech/beaper webpage for additional BEAPER Pico starter
programs and beginner programming activities.
"""

# Import machine and time functions
from machine import Pin, PWM, ADC
import time

# Built-in Raspberry Pi Pico LED
LED = Pin("LED", Pin.OUT)

# BEAPER Pico Educational Starter I/O devices
SW2 = Pin(0, Pin.IN, Pin.PULL_UP)
SW3 = Pin(1, Pin.IN, Pin.PULL_UP)
SW4 = Pin(2, Pin.IN, Pin.PULL_UP)
SW5 = Pin(3, Pin.IN, Pin.PULL_UP)
LED2 = Pin(10, Pin.OUT)
LED3 = Pin(11, Pin.OUT)
LED4 = Pin(12, Pin.OUT)
LED5 = Pin(13, Pin.OUT)
BEEPER = H8OUT = PWM(Pin(14), freq = 1000, duty_u16 = 0)

# BEAPER Pico analog input devices
Q1 = Q4 = ADC(Pin(26))
Q2 = RV1 = ADC(Pin(27))
Q3 = RV2 = ADC(Pin(28))
temp_sensor = ADC(4)

# BEAPER Pico 3.3V digital I/O
H1IN = Pin(6, Pin.IN, Pin.PULL_UP)
#H1OUT = Pin(6, Pin.OUT)
#H2IN = Pin(7, Pin.IN, Pin.PULL_UP)
H2OUT = TRIG = Pin(7, Pin.OUT)
H3IN = ECHO = Pin(8, Pin.IN, Pin.PULL_UP)
#H3OUT = Pin(8, Pin.OUT)
H4IN = Pin(9, Pin.IN, Pin.PULL_UP)
#H4OUT = Pin(9, Pin.OUT)

# BEAPER Pico 5V digital/servo outputs
#H5OUT = Pin(20, Pin.OUT)
SERVO1 = PWM(Pin(20), freq=50, duty_u16=4916)
#H6OUT = Pin(21, Pin.OUT)
SERVO2 = PWM(Pin(21), freq=50, duty_u16=4916)
H7OUT = Pin(22, Pin.OUT)
#SERVO3 = PWM(Pin(22), freq=50, duty_u16=4916)

# Tone functions. The tone() function creates sound at the specficied frequency
# using PWM output. The tone plays until stopped using the noTone() function, or
# for the optional specified duration (in seconds). Playing a tone blocks using
# duration blocks other operations for the specified duration.
def tone(frequency, duration=None):
    BEEPER.freq(frequency)
    BEEPER.duty_u16(32768)
    if duration is not None:
        time.sleep(duration)
        noTone()

# Stops the tone. Specifying an optional duration pauses for the duration of
# time specified (in seconds, and blocks other operations for the duration).
def noTone(duration=None):
    BEEPER.duty_u16(0)
    if duration is not None:
        time.sleep(duration)

# Maps a value within the input range to the output range.
def map(value, in_min, in_max, out_min, out_max):
    return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

# Servo position functions. Creates continuous servo pulses using PWM. Maps input
# degree values to PWM puslewidths. Un-comment the appropriate duty_u16 duty cycle
# to map input the required input range (0-90 or 0-180 degrees) to the output pulse
# length appopriate for your type of servo.
def servo1_position(deg):
    SERVO1.duty_u16(map(deg, 0, 90, 3277, 6554))  # 1-2ms pulses, 90 deg. input, 90 deg. servo output
    # SERVO1.duty_u16(map(deg, 0, 180, 3277, 6554))  # 1-2ms pulses, 180 deg. input, 90 deg. servo output
    # SERVO1.duty_u16(map(deg, 0, 180, 1782, 8192))  # 544us-2500us pulses, 180 deg. input and servo output
    # SERVO1.duty_u16(map(deg, 0, 180, 1638, 8192))  # 500us-2500us pulses, 180 deg. input and servo output

def servo2_position(deg):
    SERVO2.duty_u16(map(deg, 0, 90, 3277, 6554))  # 1-2ms pulses, 90 deg. input, 90 deg. servo output
    # SERVO1.duty_u16(map(deg, 0, 180, 3277, 6554))  # 1-2ms pulses, 180 deg. input, 90 deg. servo output
    # SERVO1.duty_u16(map(deg, 0, 180, 1782, 8192))  # 544us-2500us pulses, 180 deg. input and servo output
    # SERVO1.duty_u16(map(deg, 0, 180, 1638, 8192))  # 500us-2500us pulses, 180 deg. input and servo output

def servo3_position(deg):
    SERVO3.duty_u16(map(deg, 0, 90, 3277, 6554))  # 1-2ms pulses, 90 deg. input, 90 deg. servo output
    # SERVO1.duty_u16(map(deg, 0, 180, 3277, 6554))  # 1-2ms pulses, 180 deg. input, 90 deg. servo output
    # SERVO1.duty_u16(map(deg, 0, 180, 1782, 8192))  # 544us-2500us pulses, 180 deg. input and servo output
    # SERVO1.duty_u16(map(deg, 0, 180, 1638, 8192))  # 500us-2500us pulses, 180 deg. input and servo output

# SONAR range function with maximum range limit and ECHO pin error checking.
# Returns the range of the closest target in cm. The 'max' parameter limits
# the search range to objects no farther than 'max' cm. The function returns
# -1 if a previous ranging operation is still in progress, 0 if no target is
# found within the specified max range, or returns the range to the closest
# target in cm.
# Example application:
# range_cm = sonar_range(100)   # Find closest target within 100 cm
def sonar_range(max):
    # Check if previous ECHO has finished
    if ECHO.value() == 1:
        return -1   # ECHO in progress (wait 10ms after ECHO ends before re-triggering)
    
    # Create TRIG pulse
    TRIG.value(1)
    time.sleep_us(10)
    TRIG.value(0)
    
    # Wait for ECHO to go high. HC-SR04P (3.3V-capable modules, also labelled as
    # RCWL-9610A 2022) delay for approximately 2300us after TRIG pulse ends
    # before ECHO pulse starts.
    duration = machine.time_pulse_us(ECHO, 0, 2500)
    if duration < 0:
        return duration # ECHO didn't start. Return error code.
    
    # Time ECHO pulse. Set time-out value to max range.
    duration = machine.time_pulse_us(ECHO, 1, (max + 1) * 58)
    if duration < 0:
        return 0    # Return 0 if distance is > max range
    
    # Return range to target in cm
    return duration / 58
        
# Pico LED on
LED.value(1)

# Start-up sound
tone(1000, 0.1)

# Brief instructions
print("Starting BEAPER Pico")
print("SW2 - LED sequence and tones")
print("SW3 - light LED 2")
print("SW4 - light LED 5")
print("SW5 - Pico LED and tone")
print("")
time.sleep(1)

# Set timers
servo_timer = time.ticks_ms()
sensor_timer = time.ticks_ms()

while True:
    # Chase LEDs
    if SW2.value() == 0:
        LED2.value(1)
        tone(523)
        time.sleep(0.1)
        LED3.value(1)
        tone(659)
        time.sleep(0.1)
        LED4.value(1)
        tone(784)
        time.sleep(0.1)
        LED5.value(1)
        tone(1047)
        time.sleep(0.1)
        
        LED2.value(0)
        tone(2093)
        time.sleep(0.1)
        LED3.value(0)
        tone(4186)
        time.sleep(0.1)
        LED4.value(0)
        tone(8372)
        time.sleep(0.1)
        LED5.value(0)
        noTone()
        time.sleep(0.1)

    if SW3.value() == 0:
        LED2.value(1)
    else:
        LED2.value(0)
    
    if SW4.value() == 0:
        LED5.value(1)
    else:
        LED5.value(0)
    
    if SW5.value() == 0:
        LED.value(0)
        tone(1000, 0.1)
        LED.value(1)
        tone(2000, 0.1)
        LED.value(0)
        tone(3000, 0.1)
        LED.value(1)
    
    # Update servo inputs every 20ms
    if time.ticks_diff(time.ticks_ms(), servo_timer) > 20:
        # Reset servo_timer
        servo_timer = time.ticks_ms()
        # Update servos
        rv1_pos = RV1.read_u16()
        rv1_angle = map(rv1_pos, 0, 65535, 0, 90)
        servo1_position(rv1_angle)
        rv2_pos = RV2.read_u16()
        rv2_angle = map(rv2_pos, 0, 65535, 0, 90)
        servo2_position(rv2_angle)

    # Update SONAR range and analog input every 500ms
    if time.ticks_diff(time.ticks_ms(), sensor_timer) > 500:
        # Reset sensor_timer
        sensor_timer = time.ticks_ms()
        # Get and print SONAR range
        range_cm = sonar_range(100)
        print("Range:", int(range_cm), "cm")
        # Read and print analog input levels
        lightLevel = Q4.read_u16()
        rawTemp = temp_sensor.read_u16()
        print("Light level: ", lightLevel)
        print("Temp level: ", rawTemp)
        print("RV1 position: ", rv1_pos)
        print("RV2 position: ", rv2_pos)
        print("")
