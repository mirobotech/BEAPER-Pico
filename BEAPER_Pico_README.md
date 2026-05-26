# BEAPER_Pico.py

Board support module for the [mirobo.tech](https://mirobo.tech) **BEAPER Pico** circuit.

## What is BEAPER Pico?

**BEAPER** (Beginner Electronics and Programming Educational Robot) **Pico** is a fully-integrated beginner circuit designed for learning Raspberry Pi Pico programming and robotics using Thonny or other MicroPython IDEs.

`BEAPER_Pico.py` configures the Pico's GPIO pins for all of BEAPER Pico's on-board hardware and provides simple helper functions so beginners can focus on learning programming concepts first — no special libraries or hidden magic required.

## Compatible Hardware

BEAPER_Pico.py supports any Raspberry Pi Pico family module:

- Raspberry Pi Pico
- Raspberry Pi Pico 2
- Raspberry Pi Pico W
- Raspberry Pi Pico 2 W

## On-Board Hardware

| Hardware | Details |
|---|---|
| Pushbutton switches | 4 user buttons (SW2–SW5) with internal pull-ups |
| LEDs | 4 user LEDs (LED2–LED5), shared with motor driver |
| Piezo buzzer | PWM tone generation (LS1) |
| Motor driver | SH754410NE — two DC motors forward/reverse, or one bipolar stepper |
| Analog potentiometers | Two pots (RV1, RV2) — jumper-selectable |
| Ambient light sensor | TEPT4400 (Q4) — jumper-selectable |
| Floor/line sensors | IR LED + phototransistor modules (Q1, Q2, Q3) — jumper-selectable |
| SONAR header | 3.3V I/O headers H1–H4 for HC-SR04P ultrasonic distance sensor |
| Servo headers | Three 5V servo/output headers (H5–H7) |
| I2C/QWIIC connector | JST-SH connector for 3.3V I2C devices |
| LCD/SPI header | Optional 1.54" 240×240 ST7789 TFT LCD display |
| Pico LED | On-board Raspberry Pi Pico LED |

## Getting Started

1. Copy `BEAPER_Pico.py` to your Raspberry Pi Pico (e.g. using Thonny).
2. Import the module at the top of your program:

```python
from BEAPER_Pico import *
```

3. Start using the helper functions — no additional setup needed.

## Analog Jumper Settings

BEAPER Pico has on-board jumpers that select which analog devices are connected to the ADC pins. **Set jumpers before running programs that use analog inputs.**

| Jumper position | ADC0 (GP26) | ADC1 (GP27) | ADC2 (GP28) |
|---|---|---|---|
| **Enviro.** | Light sensor Q4 | Potentiometer RV1 | Potentiometer RV2 |
| **Robot** | Floor sensor Q1 | Line sensor Q2 | Floor/line sensor Q3 |

## Function Reference

### Pico On-Board LED

```python
pico_led_on()       # Turn Pico LED on
pico_led_off()      # Turn Pico LED off
pico_led_toggle()   # Toggle Pico LED
```

### User LEDs

> **Note:** LED pins are shared with the motor driver. Do not use LEDs and motors at the same time.

```python
leds_on()           # Turn all four LEDs on
leds_off()          # Turn all four LEDs off

LED2.value(1)       # Control individual LEDs directly
LED3.toggle()
```

Individual LED objects: `LED2`, `LED3`, `LED4`, `LED5`

A tuple of all LEDs is available for iteration: `LEDS`

### Pushbutton Switches

Buttons use internal pull-up resistors — **pressed = 0, released = 1**.

```python
if SW2.value() == 0:    # Check if SW2 is pressed
    print("SW2 pressed")
```

Individual switch objects: `SW2`, `SW3`, `SW4`, `SW5`

A tuple of all switches is available for iteration: `SWITCHES`

### Motors

> **Note:** Motor pins are shared with LED pins. Do not use LEDs and motors at the same time.

```python
motors_stop()           # Stop both motors

left_motor_forward()    # Left motor forward
left_motor_reverse()    # Left motor reverse
left_motor_stop()       # Stop left motor

right_motor_forward()   # Right motor forward
right_motor_reverse()   # Right motor reverse
right_motor_stop()      # Stop right motor
```

> The actual forward/reverse direction of each motor depends on its physical wiring to CON1.

### Piezo Buzzer

```python
tone(frequency)             # Start a continuous tone (Hz)
tone(frequency, duration)   # Play a tone for duration (ms), then stop
noTone()                    # Stop the tone
noTone(duration)            # Stop the tone, then pause (ms)
beep()                      # Play a 1000 Hz beep for 100 ms
beep(duration)              # Play a 1000 Hz beep for duration (ms)
```

### Analog Inputs

```python
light_level()   # Ambient light sensor Q4 (JP1 = Enviro.) — brighter → higher
RV1_level()     # Potentiometer RV1 (JP2 = Enviro.) — clockwise → higher
RV2_level()     # Potentiometer RV2 (JP3 = Enviro.) — clockwise → higher

Q1_level()      # Floor sensor Q1 (JP1 = Robot) — higher reflectivity → higher
Q2_level()      # Line sensor Q2 (JP2 = Robot) — higher reflectivity → higher
Q3_level()      # Floor/line sensor Q3 (JP3 = Robot) — higher reflectivity → higher
```

All analog functions return a 16-bit value (0–65535).

### System Sensors

```python
VSYS_volts()        # Supply voltage in volts (reads VSYS / 3 on GP29)
mcu_temperature()   # Raspberry Pi Pico die temperature in °C
```

### SONAR Distance Sensor (HC-SR04P)

Connect a 3.3V HC-SR04P module to headers H2 (TRIG) and H3 (ECHO).

```python
distance = sonar_range()            # Measure distance, default max 100 cm
distance = sonar_range(200)         # Measure distance, max 200 cm
```

Return values:

| Value | Meaning |
|---|---|
| > 0 | Distance to nearest target in cm |
| 0 | No target detected within max range |
| -1 | Timeout waiting for ECHO to start |
| -2 | Previous ECHO pulse still in progress |

### Servos

```python
set_servo(SERVO1, 45)   # Set SERVO1 to 45 degrees (0–90)
set_servo(SERVO2, 0)    # Set SERVO2 to 0 degrees
set_servo(SERVO3, 90)   # Set SERVO3 to 90 degrees
```

Servo objects: `SERVO1`, `SERVO2`, `SERVO3` (connected to H5, H6, H7)

A tuple of all servos is available for iteration: `SERVOS`

Default pulse range is 1000–2000 µs over 90°. Adjust `SERVO_MIN_US`, `SERVO_MAX_US`, and `SERVO_RANGE` constants for your servo if needed. Servos initialize to the centre position (≈1.5 ms pulse) — verify this is safe for your application before connecting servos.

### I2C / QWIIC

```python
devices = QWIIC.scan()      # Scan for I2C devices on connector J4
```

The `QWIIC` object is a standard MicroPython `I2C` instance on GP4 (SDA) and GP5 (SCL) and is compatible with any 3.3V I2C or QWIIC device.

### Digital I/O Headers

Headers H1–H4 provide 3.3V digital I/O via GP6–GP9 and can be used as general-purpose inputs or outputs in addition to their SONAR role.

```python
H1 = Pin(H1_PIN, Pin.OUT)   # Example: configure H1 as output
H4 = Pin(H4_PIN, Pin.IN)    # Example: configure H4 as input
```

Pin constants: `H1_PIN` (6), `H2_PIN` (7), `H3_PIN` (8), `H4_PIN` (9)

## GPIO Pin Map

| GPIO | Function |
|---|---|
| GP0 | SW2 pushbutton (pull-up) |
| GP1 | SW3 pushbutton (pull-up) |
| GP2 | SW4 pushbutton (pull-up) |
| GP3 | SW5 pushbutton (pull-up) |
| GP4 | I2C SDA (QWIIC J4) |
| GP5 | I2C SCL (QWIIC J4) |
| GP6 | H1 digital I/O |
| GP7 | H2 digital I/O / SONAR TRIG |
| GP8 | H3 digital I/O / SONAR ECHO |
| GP9 | H4 digital I/O |
| GP10 | LED2 / Motor M1A (left motor A) |
| GP11 | LED3 / Motor M1B (left motor B) |
| GP12 | LED4 / Motor M2A (right motor A) |
| GP13 | LED5 / Motor M2B (right motor B) |
| GP14 | Piezo buzzer LS1 |
| GP15 | LCD DC |
| GP16 | LCD CIPO / backlight |
| GP17 | LCD CS |
| GP18 | LCD SCK |
| GP19 | LCD COPI |
| GP20 | H5 servo output |
| GP21 | H6 servo output |
| GP22 | H7 servo output |
| GP26 / ADC0 | Light sensor Q4 or floor sensor Q1 (jumper) |
| GP27 / ADC1 | Potentiometer RV1 or line sensor Q2 (jumper) |
| GP28 / ADC2 | Potentiometer RV2 or floor/line sensor Q3 (jumper) |
| GP29 / ADC3 | VSYS voltage monitor (internal) |
| ADC4 | RP2 die temperature sensor (internal) |

## License

See [LICENSE](LICENSE) for details.
