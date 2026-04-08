/* =============================================================================
BEAPERPico.h
March 21, 2026

Board header file for the mirobo.tech BEAPER Pico circuit.

This header defines Raspberry Pi Pico's GPIO pins for BEAPER Pico's
on-board circuits and provides simple helper functions to enable
beginners to focus on learning programming concepts more quickly.
(A similar MicroPython board module is also available for BEAPER Pico.)

BEAPER Pico hardware notes:
- Button switches use internal pull-up resistors (so pressed == LOW)
- LEDs and motor driver inputs share I/O pins
- Analog jumpers on BEAPER Pico must be set to connect sensors to pins:
  - Enviro. position selects light sensor Q4, and pots RV1 and RV2
  - Robot position selects floor/line phototransistors Q1, Q2, and Q3
==============================================================================*/

#ifndef BEAPERPICO_H
#define BEAPERPICO_H

/* =====================================
 * Raspberry Pi Pico Module LED
 * ====================================*/
// Raspberry Pi Pico on-board LED pre-defined in the Arduino Pico core.
// NOTE: On Pico W and Pico 2 W, LED_BUILTIN is connected through the
// wireless chip and requires the WiFi library to be initialized first.

// LED_BUILTIN            // On-board LED


/* =====================================
 * LED Pins
 * ====================================*/
// IMPORTANT: LED pins are shared with the motor controller. Using the
// LEDs while the motors are active will affect motor behavior!

const uint8_t LED2 = 10;  // M1A (Motor 1 = left motor)
const uint8_t LED3 = 11;  // M1B
const uint8_t LED4 = 12;  // M2A (Motor 2 = right motor)
const uint8_t LED5 = 13;  // M2B

const uint8_t LEDS[] = {LED2, LED3, LED4, LED5};  // Array of all LED pins
const uint8_t NUM_LEDS = 4;

inline void leds_on()
{
    digitalWrite(LED2, HIGH);
    digitalWrite(LED3, HIGH);
    digitalWrite(LED4, HIGH);
    digitalWrite(LED5, HIGH);
}

inline void leds_off()
{
    digitalWrite(LED2, LOW);
    digitalWrite(LED3, LOW);
    digitalWrite(LED4, LOW);
    digitalWrite(LED5, LOW);
}


/* =====================================
 * Pushbutton Pins (Active LOW)
 * ====================================*/

const uint8_t SW2 = 0;
const uint8_t SW3 = 1;
const uint8_t SW4 = 2;
const uint8_t SW5 = 3;

const uint8_t SWITCHES[] = {SW2, SW3, SW4, SW5};  // Array of all switch pins
const uint8_t NUM_SWITCHES = 4;


/* =====================================
 * Motor Pins
 * ====================================*/
// IMPORTANT: Motor output pins are shared with the LEDs. Using the LEDs
// while driving the motors will affect motor behaviour!

const uint8_t M1A = 10;   // Left motor terminal A
const uint8_t M1B = 11;   // Left motor terminal B
const uint8_t M2A = 12;   // Right motor terminal A
const uint8_t M2B = 13;   // Right motor terminal B

// Motor helper functions
// Call pinMode() for all motor pins in setup() before using these
// functions. Motor pins share I/O with LED pins, so a single set
// of pinMode() calls covers both LEDs and motors.
//
// Suggested setup() pinMode calls:
//   pinMode(LED2, OUTPUT);   // LED2 / M1A
//   pinMode(LED3, OUTPUT);   // LED3 / M1B
//   pinMode(LED4, OUTPUT);   // LED4 / M2A
//   pinMode(LED5, OUTPUT);   // LED5 / M2B

inline void motors_stop()
{
    digitalWrite(M1A, LOW);
    digitalWrite(M1B, LOW);
    digitalWrite(M2A, LOW);
    digitalWrite(M2B, LOW);
}

inline void left_motor_forward()
{
    digitalWrite(M1A, HIGH);
    digitalWrite(M1B, LOW);
}

inline void left_motor_reverse()
{
    digitalWrite(M1A, LOW);
    digitalWrite(M1B, HIGH);
}

inline void left_motor_stop()
{
    digitalWrite(M1A, LOW);
    digitalWrite(M1B, LOW);
}

inline void right_motor_forward()
{
    digitalWrite(M2A, LOW);
    digitalWrite(M2B, HIGH);  // Opposite of left_motor_forward()
}

inline void right_motor_reverse()
{
    digitalWrite(M2A, HIGH);  // Opposite of left_motor_reverse()
    digitalWrite(M2B, LOW);
}

inline void right_motor_stop()
{
    digitalWrite(M2A, LOW);
    digitalWrite(M2B, LOW);
}


/* =====================================
 * Piezo Beeper Pin
 * ====================================*/

const uint8_t LS1 = 14;   // BEAPER Pico piezo beeper LS1 (also wired to H8)

inline void beep()
{
    tone(LS1, 1000, 100);  // Play a short beep
}


/* =====================================
 * 3.3V I/O Expansion Header Pins
 * ====================================*/

const uint8_t H1 = 6;     // Header H1
const uint8_t H2 = 7;     // Header H2 (shared with SONAR TRIG)
const uint8_t TRIG = 7;   // Ultrasonic SONAR distance sensor TRIG(ger) output
const uint8_t H3 = 8;     // Header H3 (shared with SONAR ECHO)
const uint8_t ECHO = 8;   // Ultrasonic SONAR distance sensor ECHO input
const uint8_t H4 = 9;     // Header H4


/* =====================================
 * 5V Output Expansion Header Pins
 * ====================================*/
// NOTE: H5, H6, and H7 are independent 5V output pins suitable for servos.
// H8 shares the piezo beeper pin LS1 (GP14). Disable the buzzer PWM before
// using H8 as a servo or digital output: noTone(LS1);

const uint8_t H5 = 20;    // 5V output / Servo 1
const uint8_t H6 = 21;    // 5V output / Servo 2
const uint8_t H7 = 22;    // 5V output / Servo 3
const uint8_t H8 = 14;    // 5V output / Servo 4 (shares piezo beeper LS1)


/* =====================================
 * SONAR Distance Sensor Functions
 * ====================================*/
// NOTE: TRIG (GP7) and ECHO (GP8) share H2 and H3 respectively.

// Call sonar_setup() once in setup() to configure the SONAR pins.
inline void sonar_setup()
{
    pinMode(TRIG, OUTPUT);
    digitalWrite(TRIG, LOW);
    pinMode(ECHO, INPUT);
}

// sonar_range(max_range) - Returns the distance to the nearest
//     target within max_range in cm (defaults to 1m)
//
// Returns either:
//     distance (cm) - closest target within max_range
//     0             - no target detected within max_range
//     -1            - time-out waiting for ECHO to start
//     -2            - previous ECHO is still in progress

inline float sonar_range(int max_range = 100)
{
    // Return -2 if a previous ECHO pulse is still in progress
    if (digitalRead(ECHO) == HIGH)
        return -2;

    // Make a 10 us TRIG pulse to start a range measurement
    digitalWrite(TRIG, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG, LOW);

    // Convert max_range plus 1cm margin to round trip time-out
    // in microseconds (~29us/cm one way)
    unsigned long max_us = (max_range + 1) * 58;

    // Wait up to 2500us for ECHO to go HIGH after TRIG.
    // (Necessary for 3.3V HC-SR04P/RCWL-9610A SONAR modules.)
    unsigned long start_us = micros();
    while (digitalRead(ECHO) == LOW)
    {
        if (micros() - start_us > 2500)
            return -1;      // ECHO did not start
    }

    // Measure ECHO pulse duration.
    start_us = micros();
    while (digitalRead(ECHO) == HIGH)
    {
        if (micros() - start_us > max_us)
            return 0;       // No target within max_range
    }

    // Convert ECHO duration to distance. (~29us/cm one way)
    return (micros() - start_us) / 58.0f;
}


/* =====================================
 * QWIIC/I2C Connector J4
 * ====================================*/
// NOTE: QWIIC uses GP4 (SDA) and GP5 (SCL).
// Call Wire.begin() in setup() to initialise the I2C bus before use.

const uint8_t QWIIC_SDA = 4;  // I2C SDA
const uint8_t QWIIC_SCL = 5;  // I2C SCL


/* =====================================
 * Analog I/O Pins
 * ====================================*/
// IMPORTANT: On-board analog jumpers must be set to select each input.

// NOTE: The Arduino Pico core defaults to 10-bit ADC resolution (0-1023),
// matching the default resolution of other Arduino boards. Use
// analogReadResolution(12) in setup() for 12-bit results (0-4095).

const uint8_t Q1 = A0;    // Left floor/line sensor phototransistor Q1 (JP1 - Robot)
const uint8_t Q4 = A0;    // Ambient light sensor Q4 (JP1 - Enviro.)
const uint8_t Q2 = A1;    // Line sensor phototransistor Q2 (JP2 - Robot)
const uint8_t RV1 = A1;   // Potentiometer RV1 (JP2 - Enviro.)
const uint8_t Q3 = A2;    // Right floor/line sensor phototransistor Q3 (JP3 - Robot)
const uint8_t RV2 = A2;   // Potentiometer RV2 (JP3 - Enviro.)

// Analog helper functions: return 10-bit (0-1023) values by default.
// If analogReadResolution(12) is set in setup(), change 1023 to 4095.

inline int light_level() { return 1023 - analogRead(Q4); }   // Brighter -> higher values (JP1 - Enviro.)
inline int Q1_level()    { return 1023 - analogRead(Q1); }   // Higher reflectivity -> higher values (JP1 - Robot)
inline int Q2_level()    { return 1023 - analogRead(Q2); }   // Higher reflectivity -> higher values (JP2 - Robot)
inline int RV1_level()   { return analogRead(RV1); }         // Clockwise -> higher values (JP2 - Enviro.)
inline int Q3_level()    { return 1023 - analogRead(Q3); }   // Higher reflectivity -> higher values (JP3 - Robot)
inline int RV2_level()   { return analogRead(RV2); }         // Clockwise -> higher values (JP3 - Enviro.)

// Raspberry Pi Pico system voltage and die temperature

inline float VSYS_volts()
{
    // Read the VSYS supply voltage in volts.
    // VSYS is divided by 3 before reaching ADC input A3 (GP29).
    return analogRead(A3) * 9.9f / 1023;
}

inline float temp_C()
{
    // Read the RP2040/RP2350 die temperature in degrees C.
    return analogReadTemp();
}

#endif