Assignment 1
================================

This is a possible implementation of the first assignment of Research Track 1 course.

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
* `silver_box = int(0)`: number referred to the silver colour
* `golden_box = int(1)`: number referred to the golden colour
* `timer_change = int(50)`: initial value of the timer to make the robot change its target of stacked
* `timer_end = int(30)`: initial value of the timer to make the program end
* `list_token_silver = list()`: list of the silver token already paired
* `list_token_gold = list()`: list of the golden token already paired
* `color_token = [MARKER_TOKEN_SILVER, MARKER_TOKEN_GOLD]`: list of the color code of the tokens
* `a_th = 2.0`: threshold to control the angular orientation of the robot
* `d_th = 0.4`: threshold to control the linear distance of the robot

The code is divided into separate functions:

* `main()`: manages the robot so that it will reach the goal of having silver and golden boxes paired.

```python
set initial values for number of the color, grab and release variable, timer to change and timer to end

while timer to end the research is grater or equal to 0:

    if the number of the color is equal to 0 (silver) and release is true:
        reset timer to end

        call grab_box function

        if grab is true:
            change number of the color into 1 (gold)
            chenge release variable into false

    if the number of the color is equal to 1 (gold) and grab variable is true:
        reset timer to end
        
        call release_box function

        if release is true:
            change number of the color into 0 (silver)
            chenge grab variable into false

exit the program when the timer to end is over
```

* `grab_box(num_colour_box, success_grab_silver, timer_to_end)`: look for a box of the specified colour, reach it and grab it. 
Manage the timer to change target in case the robot is stacked and the timer to end the program.
This function calls several time the functions `find_token(col_num)`, `drive(speed, seconds)` and `turn(speed, seconds)`.

```python
reset timer to chenge target
	
while grab variable is false and the timer to end is grater or equal to 0:

        if any token is found:
            turn  and look for another box
            decrease the timer to end
            
        elif the robot is enought close to the target box:
            add the code of the box to the list of the silver boxes paired
            grab the box and upadate grab variable
            reset the timer to change box
            
        elif the taget box is on the right of the robot:
            turn right
            decrease the timer to change
            
        elif the taget box is on the left of the robot:
            turn left
            decrease the timer to chenge
            
        elif the robot is alligned and not enought closed to the target box:
            move forward
            decrease the timer to change

        if the timer to change is less than 0:
            change target by driving back and turn the robot
            reset the timer to change target
            reset the timer to end the program
	
return true the robot success to grab the box, false if not; the value of the timer to end the program
```

* `release_box(num_colour_box, success_release_silver, timer_to_end)`: look for a box of the specified colour, reach it and release the box near the target one. 
Manage the timer to change target in case the robot is stacked and the timer to end the program.
This function calls several time the functions `find_token(col_num)`, `drive(speed, seconds)` and `turn(speed, seconds)`.

```python
reset timer to chenge target

while release variable is false and timer to end is grater or equal to 0:

            if any token is found:
                turn and look for another box
                decrease the timer to end
                
            elif the robot is enought close to the target box:
                add the code of the box to the list of the golden boxes paired
                release the box and upadate grab variable
                drive back and turn right
                reset the timer to change box
                
            elif the taget box is on the right of the robot:
                turn right
                decrease the timer to change
                
            elif the taget box is on the left of the robot:
                turn left
                decrease the timer to change
                
            elif the robot is alligned and not enought closed to the target box:
                move forward
                decrease the timer to change

            if the timer to change is less than 0:
                change target by driving back and turn the robot
                reset the timer to change
                reset the timer to end the program

return true the robot success to release the box, false if not; the value of the timer to end the program
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
if the robot sees a box and it is not the target one:
    turn right to avoid it
```
