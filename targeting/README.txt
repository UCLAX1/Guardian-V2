UCLA ASME X1 Robotics Ð Guardian V2 Targeting Program File List
Last updated by Hayato Kato on September 15, 2020

** Disclaimer: There were two main iterations of the algorithm: one using the old stepper library, and one using our custom stepper library. The most current version utilizes the custom stepper library that allows precise control over both steppers simultaneously. Also, there were two different ADC chips used along the development. The most current version uses the ADS1115 chip, which has a 16 bit resolution.

=== Program List ===

• DEMO_PROGRAM.py - Demo program used during engineering day to show off the capabilities of the hardware. Hard-coded in the path for various shapes and cycles through them randomly. Still uses the first iteration of the algorithm that uses the old stepper library.

• adc_test.py - Simple test program that looks at how to use the ADC library. Simply prints out the ADC values in the terminal window. Uses the new ADC chip (ADS1115) which has 16 bits of resolution.

• circle.py - First iteration of a demo program that attempted to show the capabilities of the hardware. Used the original stepper motor library that only allowed control over one step at a time, resulting in a very low-resolution circle that clearly showed jagged edges. Also used BresenhamÕs Line Generation Algorithm to try to smooth out the diagonal laser motion. 

• circle2.py - Same basic logic and algorithm as circle.py, but draws a different path. Was testing one axis at a time by disabling the y-axis and setting it constant.

• coords.py - First version of the laser targeting system, where there are no interpolation in between consecutive position commands. Due to how quickly the moveToCoords() function runs in comparison to the receive_data() function, the feedback loop fails and seems to struggle in consistent laser tracking of the target object. The updated version is named Coords2.py.

• coords2.py - Working version of laser detection and targeting, where the target position is temporarily set to be the center of the screen at all times. Unlike the prior version, the moveToCoords() function has a while loop in it that predicts the correct motor position based on the most current feedback information and interpolates until the next update is received. The updated version where the entire program is cleaned up is named pi_zero.py.

• demo.py - Simpler version of the demo program first made before DEMO_PROGRAM.py. Although outdated by the newer program, still draws out several shape patterns in order. Also uses the old stepper library that makes the movement jerky.

• input_pot_goal.py - Asks for user input for the X and Y position goals and moves the stepper motor until the potentiometers read the correct angle values. 

• lineteststepper.py - Another initial demo program that attempted to demonstrate the capabilities of the BresenhamÕs Line Generation Algorithm. Draws several straight diagonal lines.

• pi_zero.py - Cleaned up version of the current working program. In order to change the targeting goal, the link_coords variable should be updated with the correct values received from the computer on line 171.

• pi_zero2.py - Next version of the current working program, where an initial centering sequence relying on the potentiometers is tentatively added. This version is currently not confirmed to work, thus separated from the original working file. 

• pot-to-step.py - An experimenting program that was used to calculate the correspondence between the potentiometer values and the stepper motor counts. It works by moving the stepper motors a certain number of steps and recording the change in potentiometer values.

• pot_stepper_test.py - First test of stepper feedback, but had limited success due to the little resolution of the first ADC we used (MCP3008).

• pottest.py - Simple test program that looks at how to use the ADC library. Simply prints out the ADC values in the terminal window. Uses the old ADC chip (MCP3008) which only has 10 bits of resolution.

• slowLineTest.py - Runs the same algorithm as lineteststepper.py, but slows the delay between stepper steps in order to visualize the BresenhamÕs Line Generation Algorithm.

• smoothSteps.py - Base program algorithm referenced from Tucker ShannonÕs LaserPi project (https://github.com/tuckershannon/LaserPi). The original program was adapted to work with our hardware setup and modified to work accordingly. This became the basis for the laserÕs movement in all current iterations of the laser targeting system.

• smooth_pot_step.py - Another version of the stepper feedback test program, where a pre-calculated conversion ratio between the stepper motor counts and the potentiometer values were used to make the movement smoother. Ultimately led to the decision to use an ADC with a higher resolution.

• teststepper.py - Test program used to learn how to use the old stepper library. Had limited functionality due to how it does not give users precise control simultaneously over two steppers.
