"""
================================================================================
Beginner Activity 4: Constants and Variables [Activity_B04_Constants_Variables.py]
February 5, 2026

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

1.  There are a lot of new and important concepts to cover in this
    program, so let's start at the top with the simplest one. First,
    program constants:

# --- Program Constants ----------------
BLINK_DELAY = const(200)

    A program constant is simply an un-changing, named value in a
    program. In this program, the named constant 'BLINK_DELAY' is
    defined as 200 – and it won't change while the program runs.
    (Constants are often written in ALL_CAPS to distinguish them
    from variables, which we'll find out about below.)

    It might seem like extra work to write BLINK_DELAY instead of
    200, but using a name instead of a number provides two important
    benefits. First, the name 'BLINK_DELAY' is more descriptive
    than 200, providing instrinsic meaning for anyone reading the
    program. Second, using the BLINK_DELAY constant in all instances
    of the delays allows all of the delay values to be changed
    simultaneously with just one edit at the top of the program.

    Run the program. Then, change BLINK_DELAY to 100 and run it
    again. Then, try 50. Imagine how much longer it would have
    taken to make the changes in every delay statement!

2.  The next important concept in this program is the use of
    Boolean true/false variable expressions:

# --- Program Variables ----------------
SW2_pressed = False
display_pattern = False

    Both of these variable names have been set to be 'False', but
    either could just as easily have been set to be 'True'. In fact,
    since they don't have to be constant or maintain their value,
    they can vary, or be changed, during program execution.

    Let's look at the display_pattern variable first. When SW2 is
    pressed, the display_pattern variable gets set to True. The next
    if statment takes a short-cut. Instead of being written as a
    typical conditional expression:

  if display_pattern == True:

    ... it's simply written as:
    
  if display_pattern:

    During program execution, the expression 'display_pattern == True'
    is evaluated by MicroPython as being either True or False, and if
    the result of the evaluation is True, the contents of the if
    structure are executed. Since the display_pattern variable itself
    can be set to be True or False, the if condition can evaluate the
    variable instead of the expression (since display_pattern == True
    will only be true when display_pattern is, actually, True).

    The 'if display_pattern:' condition runs the light show every
    cycle of the 'while True:' (another expression-less expression!)
    loop as long as the display_pattern variable is True. Pressing
    SW2 sets the display_pattern variable to True, but there is no
    corresponding else: statement to make the display_pattern
    variable False.
    
    Explain why the LED animation stops after SW2 is released.

3.  The third important concept blends the features and benefits
    of the previous two. First, the 'SW2_pressed' variable is
    defined as a Boolean variable by setting it to be False:

SW2_pressed = False

    Next, SW2_pressed is assigned its True or False value by
    evaluating the expression 'beaper.SW2.value() == 0', as shown
    in the first statement of the main while loop:
    
  SW2_pressed = (beaper.SW2.value() == 0)
  
    The '== 0' causes this expression to evaluate if the value of
    the SW2 pin is 0, which it will be if it's pressed. (This is due
    to SW2 being an active-low pushbutton created using a pull-up
    resistor input circuit.) If SW2's value is 0, the expression
    being evaluated will be True, and this makes the SW2_pressed
    variable True, exactly as with display_pattern, above.

    Exactly as with BLINK_DELAY, the SW2_pressed variable name also
    carries meaning, since SW2_pressed will be True only when SW2 is
    actually pressed.

    How could a program check for a pushbuton being released? Create
    an appropriate variable name and expression to describe SW2 in
    its un-pressed state.
    
4.  The final new concept deals with the property of consistent
    state during each individual cycle of the program's main while
    loop. It's not relevant in this program since it's just a short
    example, but imagine if SW2 had to be read multiple times, by
    multiple if conditions, during each pass through a long, complex
    main program loop. If the state of SW2 was evaluated using the
    same expression for every condition in the loop:
    
    if beaper.SW2.value() == 0:
    
    ... the button state could conceivably change between successive
    conditional checks during the same loop, resulting in inconsistent
    behaviour.
    
    In this program the expression:

    SW2_pressed = (beaper.SW2.value() == 0)
    
    ... is only evaluated once each loop cycle, and saves the result
    of its check in the SW2_pressed variable. Every subsequent check
    of SW2 can simply refer to the variable, ensuring consistent
    input state during the entire main loop cycle. And, testing the
    variable just reads nicely:

    if SW2_pressed:

    There's no ambiguity about what this expression means, it doesn't
    rely on the programmer having to remember if SW2 is an active-low
    or active-high input every time they want to add another SW2
    input condition to the main loop, and it's shorter than either 
    of the SW2 input previous expressions! 
    
5.  


Programming Activities

1.  

"""