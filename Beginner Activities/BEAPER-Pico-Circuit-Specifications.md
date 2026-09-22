# BEAPER Pico Circuit Specifications

# BEAPER Pico Circuit Introduction

BEAPER stands for Beginner Electronics and Programming Educational Robot, and Pico refers to the Raspberry Pi Pico family of circuits it’s designed for.

BEAPER Pico is a fully-integrated beginner circuit designed for teaching Raspberry Pi Pico programming and robotics using Thonny or other MicroPython IDEs.

# BEAPER Pico Circuit Hardware

BEAPER Pico  includes the following on-board hardware devices:
Raspberry Pi Pico (or Pico 2, or Pico W, or Pico 2 W) module
- 5V low-drop-out voltage regulator (U1)
- reset pushbutton (SW1)
- four user pushbuttons (SW2 - SW5)
- power LED (LED1)
- four user LEDs (LED2 - LED5)
- piezo buzzer (LS1)
- TEPT4400 ambient light sensor (Q4)
- SH754410NE motor driver (U3) capable of driving two DC motors in forward and reverse (or one bi-polar stepper motor)
- two analog potentiometers (RV1, RV2)
- two break-away optical sensor modules containing IR LEDs and phototransistor (the left module uses one LED (LED6) and one phototransistor (Q1) to act as a robot floor sensor, the right module can use one LED (LED7) and either one phototransistor (Q3) to act as a matching floor sensor, or two phototransistors (Q2, Q3) to act as a single line sensor)
- a 3.3V I/O expansion header consisting of four parallel 3-pin headers (H1 - H4) allowing an optional HC-SR04 SONAR distance sensor module to be mounted on-board
- a JST-SH I2C/QWIIC connector (J4) allowing external I2C devices to be connected
- three 5V servo/output headers (H5 - H7)
- an SPI header to connect an optional 1.54”, 240x240 pixel TFT LCD display (supports LCDs using ST7789 controllers)

## BEAPER Pico Raspberry Pi Pico GPIO Pin Mapping

GP0 - pushbutton SW2 input using internal pull-up
GP1 - pushbutton SW3 input using internal pull-up
GP2 - pushbutton SW4 input using internal pull-up
GP3 - pushbutton SW5 input using internal pull-up
GP4/SDA - I2C/QWIIC connector J4 SDA 
GP5/SCL - I2C/QUIIC connector J4 SCL
GP6 - 3.3V I/O header H1
GP7 - 3.3V I/O header H2 (dual function as HC-SR04P SONAR module TRIG output)
GP8 - 3.3V I/O header H3 (dual function as HC-SR04P SONAR module ECHO input)
GP9 - 3.3V I/O header H4
GP10 - LED D2 output, shared with motor driver 1A input (motor driver 1Y output becomes M1A - motor 1 (left motor), terminal A)
GP11 - LED D3 output, shared with motor driver 2A input (motor driver 2Y output becomes M1B - motor 1 (left motor), terminal B)
GP12 - LED D4 output, shared with motor driver 3A input (motor driver 3Y output become M2A - motor 2 (right motor), terminal A)
GP13 - LED D5 output, shared with motor driver 4A input (motor driver 4Y output becomes M2B - motor 2 (right motor), terminal B)
GP14 - piezo buzzer LS1 output
GP15 - LCD/SPI DC pin
GP16 - LCD/SPI CIPO/BL pin (used to control LCD backlight)
GP17 - LCD/SPI CS pin
GP18 - LCD/SPI SCK pin
GP19 - LCD/SPI COPI pin
GP20 - 5V servo output header H5
GP21 - 5V servo output header H6 
GP22 - 5V servo output header H7
GP26/ADC0 - jumper selectable between ambient light sensor Q4 input and left floor sensor phototransistor Q1 input
GP27/ADC1 - jumper selectable between potentiometer RV1 input and left line sensor phototransistor Q2 input
GP28/ADC2 - jumper selectable between potentiometer RV2 input and right floor/line sensor phototransistor Q3 input

# BEAPER Pico Component Placement

The BEAPER Pico circuit board is laid out in a landscape format rectangle, with the break-away optical sensor modules located at the top corners (LED D6 and phototransistor Q1 at top left, LED D7 and phototransistors Q2 and Q3 at top right).

When the optical sensor modules are broken away, the remaining top, protruding centre section of the PCB holds the QWIIC connector and the H1-H4 header connectors designed to mount the SONAR module (centred horizontally within the PCB).

Immediately below the SONAR module is the Raspberry Pi Pico, then the 240x240 pixel TFT LCD display, and a battery and motor screw terminal header strip is centred along the bottom edge of the PCB.

The ambient light sensor, potentiometers RV1 and RV2 and the analog select jumpers (along with the main power switch, reset button, and voltage regulator) are located in the space to the left of the processor, LCD, and screw terminal strip.

The piezo speaker, LEDs, pushbuttons, and 5V output headers H5-H8 are located to the right of the processor, LCD, and screw terminal strip.

## LED arrangement

The four LEDs are arranged in a horizontal line from left (D2) to right (D5) beside the LCD and are roughly in line with the top of the LCD.

## Pushbutton arrangement and labels

Pushbuttons SW2-SW5 are arranged in a diamond pattern to the right of the LCD and below the LEDs, at the following positions and with the associated silkscreen labels:

- SW2 (top), labelled with a circle
- SW3 (left), labelled with a left-facing triangle
- SW4 (right), labelled with a right-facing triangle
- SW5 (bottom), labelled with a square

