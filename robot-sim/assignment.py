from __future__ import print_function

import time
from sr.robot import *

R = Robot()

# list: Silver tokens already used 
list_token_silver = list()

# list: Gold tokens already used 
list_token_gold = list()

# list: Marker type name of the tokens 
color_token = [MARKER_TOKEN_SILVER, MARKER_TOKEN_GOLD]

# float: Threshold for the control of the orientation
a_th = 2.0

# float: Threshold for the control of the linear distance
d_th = 0.4


##############################################
# Function for setting a linear velocity
#  
# Args: speed (int): the speed of the wheels
# 	seconds (int): the time interval
##############################################
def drive(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0


##############################################
# Function for setting an angular velocity
#  
# Args: speed (int): the speed of the wheels
# 	seconds (int): the time interval
##############################################
def turn(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0


#################################################################
# Function to find the closest token with specific colour
#  
# Args: col_num (int): number of the color
# 			0 for silver token
# 			1 for gold token
# Returns: dist (float): distance of the closest token 
# 			 (-1 if no token is detected)
# 	   rot_y (float): angle between the robot and the token
# 			  (-1 if no token is detected)
# 	   code (int): code associated to the token
#################################################################
def find_token(col_num):
    dist = 100
    rot_y = 0
    code = 0
    for token in R.see():
        if token.dist < dist and token.info.marker_type == color_token[col_num]:
            if token.info.marker_type == MARKER_TOKEN_SILVER and token.info.code not in list_token_silver:
                dist = token.dist
                rot_y = token.rot_y
                code = token.info.code
            elif token.info.marker_type == MARKER_TOKEN_GOLD and token.info.code not in list_token_gold:
                dist = token.dist
                rot_y = token.rot_y
                code = token.info.code

    if dist == 100:
        return -1, -1, -1
    else:
        return dist, rot_y, code


#######################################
#
# Main function to control the robot
# 
#######################################
def main():
    num_color_box = 0
    success_release_silver = True
    success_grab_silver = False
    timer_to_change = 50
    timer_to_end = 30

    while timer_to_end >= 0:

        if num_color_box == 0 and success_release_silver:
            print("Looking for a silver box not already taken...")
            timer_to_end = 30

            while not success_grab_silver and timer_to_end >= 0:

                if find_token(num_color_box)[0] == -1 or find_token(num_color_box)[1] == -1:
                    turn(10, 1)
                    print("Searching util timer ends... " + str(timer_to_end))
                    timer_to_end -= 1
                elif find_token(num_color_box)[0] < d_th:
                    list_token_silver.append(find_token(num_color_box)[2])
                    success_grab_silver = R.grab()
                    timer_to_change = 50
                elif find_token(num_color_box)[1] > a_th:
                    turn(1, 1)
                    timer_to_change -= 1
                elif find_token(num_color_box)[1] < -a_th:
                    turn(-1, 1)
                    timer_to_change -= 1
                elif -a_th < find_token(num_color_box)[1] < a_th and find_token(num_color_box)[0] > d_th:
                    drive(35, 1)
                    timer_to_change -= 1

                if timer_to_change <= 0:
                    print("I am not able to reach the box! I'll find another one")
                    drive(-30, 2)
                    turn(40, 2)
                    timer_to_change = 50

            if success_grab_silver:
                num_color_box = 1
                success_release_silver = False

        if num_color_box == 1 and success_grab_silver:
            print("Looking for a golden box not already paired...")
            timer_to_end = 30

            while not success_release_silver and timer_to_end >= 0:

                if find_token(num_color_box)[0] == -1 or find_token(num_color_box)[1] == -1:
                    turn(10, 1)
                    print("Searching util timer ends... " + str(timer_to_end))
                    timer_to_end -= 1
                elif find_token(num_color_box)[0] < (d_th * 2):
                    list_token_gold.append(find_token(num_color_box)[2])
                    success_release_silver = R.release()
                    print("Codes of the silver box already paired: " + str(list_token_silver))
                    print("Codes of the golden box already paired: " + str(list_token_gold))
                    drive(-20, 2)
                    turn(30, 2)
                    timer_to_change = 50
                elif find_token(num_color_box)[1] > a_th:
                    turn(1, 1)
                    timer_to_change -= 1
                elif find_token(num_color_box)[1] < -a_th:
                    turn(-1, 1)
                    timer_to_change -= 1
                elif -a_th < find_token(num_color_box)[1] < a_th and find_token(num_color_box)[0] > d_th:
                    drive(35, 1)
                    timer_to_change -= 1

                if timer_to_change <= 0:
                    print("I am not able to reach the box! I'll find another one")
                    drive(-30, 2)
                    turn(40, 2)
                    timer_to_change = 50

            if success_release_silver:
                num_color_box = 0
                success_grab_silver = False

    print("\nI've finished my work! All the boxes are paired... \nBye bye!")
    exit()


main()
