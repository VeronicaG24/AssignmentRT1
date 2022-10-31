Python Robotics Simulator 
================================

This is a simple, portable robot simulator developed by [Student Robotics](https://studentrobotics.org).
Some arenas and the exercises have been modified for the Research Track I course

Installing and running
----------------------

The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, 
[PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

Once the dependencies are installed, simply run the `test.py` script to test out the simulator.

Robot API
---------

The API for controlling a simulated robot is designed to be as similar as possible to the [SR API][sr-api].

### Motors ###

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.

The Motor Board API is identical to [that of the SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

### The Grabber ###

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.

```python
success = R.release()
```

Cable-tie flails are not implemented.

### Vision ###

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).

For example, the following code lists all the markers the robot can see:

```python
markers = R.see()
print "I can see", len(markers), "markers:"

for m in markers:
    if m.info.marker_type in (MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER):
        print " - Token {0} is {1} metres away".format( m.info.offset, m.dist )
    elif m.info.marker_type == MARKER_ARENA:
        print " - Arena marker {0} is {1} metres away".format( m.info.offset, m.dist )
```

[sr-api]: https://studentrobotics.org/docs/programming/sr/

Assignment 1
================================

How to run
----------------------

To launch it, download the repository from GitHub:

```python
git clone command https://github.com/VeronicaG24/AssignmentRT1.git
```

Switch to the assignment22 branch:

```python
git checkout assignment22
```

Then, launch it from robot-sim folder:

```python
python2 run.py assignment.py
```

Requirements
----------------------

The code is designed to respect the following requirements:

1. Search and find a silver box in the environment
2. Put this silver box close to a golden box

Goal: Having silver and golden boxes distributed in pairs.

Description of the code
----------------------

Global variables are defined at the start of the code:

* `R = Robot()`: creation of the robot
* `list_token_silver = list()`: list of the silver token already paired
* `list_token_gold = list()`: list of the golden token already paired
* `color_token = [MARKER_TOKEN_SILVER, MARKER_TOKEN_GOLD]`: list of the color code of the tokens
* `a_th = 2.0`: threshold to control the angular orientation of the robot
* `d_th = 0.4`: threshold to control the linear distance of the robot

The code is divided into separate functions:

* `main()`: manages the robot so that it will reach the goal if having silver and golden boxes paired.

```python
set initial values for number of the color, grab and release variable, timer to change and timer to end

while timer to end the research is grater or equal to 0:

    if the number of the color is equal to 0 (silver) and release is true:
        reset timer to end

        while grab variable is false and the timer to end is grater or equal to 0:

            if any token is found:
                turn  and look for another box
                decrease the timer to end
                
            elif the robot is enought close to the target box:
                add the code of the box to the list of the silver boxes paired
                grab the box and upadate grab variable
                reset the timer to chenge box
                
            elif the taget box is on the right of the robot:
                turn right
                decrease the timer to chenge
                
            elif the taget box is on the left of the robot:
                turn left
                decrease the timer to chenge
                
            elif the robot is alligned and not enought closed to the target box:
                move forward
                decrease the timer to change

            if the timer to change is less than 0:
                change target by driving back and turn the robot
                reset the timer to change

        if grab is true:
            change number of the color into 1 (gold)
            chenge release variable into false

    if the number of the color is equal to 1 (gold) and grab variable is true:
        reset timer to end

        while release variable is false and timer to end is grater or equal to 0:

            if any token is found:
                turn and look for another box
                decrease the timer to end
                
            elif the robot is enought close to the target box:
                add the code of the box to the list of the golden boxes paired
                release the box and upadate grab variable
                drive back and turn right
                reset the timer to chenge box
                
            elif the taget box is on the right of the robot:
                turn right
                decrease the timer to chenge
                
            elif the taget box is on the left of the robot:
                turn left
                decrease the timer to chenge
                
            elif the robot is alligned and not enought closed to the target box:
                move forward
                decrease the timer to change

            if the timer to change is less than 0:
                change target by driving back and turn the robot
                reset the timer to change

        if release is true:
            change number of the color into 0 (silver)
            chenge grab variable into false

exit the program when the timer to end is over
```

* `drive(speed, seconds)`: commands the linear velocity of the robot, fixing the speed and how long the robot has to move.

```python
activate the motor 0 and motor 1 of the robot at the speed value received
set sleep time equal to the time value received
turn off both motors
```

* `turn(speed, seconds)`: commands the angular velocity of the robot, fixing the speed and how long the robot has to rotate.

```python
activate motor 0 of the robot at positive speed value received
activate motor 1 of the robot at negative speed value received
set sleep time equal to the time value received
turn off both motors
```

* `find_token(col_num)`: finds a token with a specific colour and code, and returns distance, relative angle and code of the token.

```python
set initial distance equal to 100
initialize rotation angle and code of the token
for every token seen by the robot:
    if the distance meausured is less the previous distance saved and the color correspond to the target one:
        if the color of the token is silver and its code is not in the list of the silver token already paired:
            set the distance
            set the relative angle
            set the code
        elif the color of the token is gold and its code is not in the list of the golden token already paired:
            set the distance
            set the relative angle
            set the code

if the distance is equal to 100:
    return -1, -1, -1
else:
    return distance, relative angle and code of the target token
```

Implemented improvements
----------------------

Some improvements have been implemented due to avoid some critical situations:

* To avoid the collision with the golden box before the release of the silver box, in the main function, where the distance to release the box is checked, I set the parameter equals to (d_th*2).

```python
elif find_token(num_color_box)[0] < (d_th * 2):
```

* To avoid hitting the box just released, the robot does a movement back and turns on its self.

```python
success_release_silver = R.release()
....
drive(-20, 2)
turn(30, 2)
....
```

* To avoid the robot to be stacked trying to grab a box that is behind another, a timer is set and when it is over the robot goes back, turns and looks for another box.

```python
timer_to_change = 50
```

* To end the searching when the boxes are all paired, a timer is set and at the end the program closes.

```python
timer_to_end = 30
```

Possible improvements
----------------------

Other improvements are possible:

* To avoid the robot to be stacked trying to grab a box that is behind another, instead of the timer, it is possible to make the robot turns around the box to be able to grab the other box.

```python
if the robot sees box in front of the target one:
    turn around to avoid the box
```

* To end the searching when the boxes are all paired, instead of the timer, it is possible to count all the boxes at the start and there are no boxes left, the program closes.

```python
if there is no box left to pair:
    exit the code
```

* To avoid hitting boxes along the path to reach a box, it is possible to turn a little right and then keep moving forward to reach the target box.

```python
if a box is seen and it is not the target:
    turn right to avoid it
```