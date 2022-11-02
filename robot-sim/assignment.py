from __future__ import print_function

import time
from sr.robot import *

R = Robot()

#int: number of the silver colour
silver_box = int(0)

#int: number of the golden colour
golden_box = int(1)

# int: Timer to make the robot change its target box
timer_change = int(50)
    
# int: Timer to end the program
timer_end = int(30)

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


######################################################################
# Function to reach and grab the closest box with specific colour
# Manage the timers to change target or to end the program
#  
# Args: num_color_box (int): number of the color
# 			      0 for silver token
# 			      1 for gold token
#	success_grab_silver (boolean): True if a box is grabbed
#					False if not grabbed
#	timer_to_end (int): value of the timer to end the program
# Returns: success_grab_silver (boolean): True if a box is grabbed
#					   False if not grabbed
# 	   timer_to_end (int): value of the timer to end the program
######################################################################
def grab_box(num_color_box, success_grab_silver, timer_to_end):
	timer_to_change = timer_change
	
	while not success_grab_silver and timer_to_end >= 0:
		if find_token(num_color_box)[0] == -1 or find_token(num_color_box)[1] == -1:
			turn(10, 1)
			print("Searching util timer ends... " + str(timer_to_end))
			timer_to_end -= 1
		elif find_token(num_color_box)[0] < d_th:
			list_token_silver.append(find_token(num_color_box)[2])
			success_grab_silver = R.grab()
			timer_to_change = timer_change
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
			timer_to_change = timer_change
	
	return success_grab_silver, timer_to_end
	

######################################################################
# Function to find and release a box close to a specific coloured box
# Manage the timers to change target or to end the program
#  
# Args: num_color_box (int): number of the color
# 			      0 for silver token
# 			      1 for gold token
#	success_release_silver (boolean): True if a box is released
#					   False if not released
#	timer_to_end (int): value of the timer to end the program
# Returns: success_release_silver (boolean): True if a box is grabbed
#					      False if not grabbed
# 	   timer_to_end (int): value of the timer to end the program
######################################################################	
def release_box(num_color_box, success_release_silver, timer_to_end):
	timer_to_change = timer_change
	
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
		        timer_to_change = timer_change
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
		         timer_to_change = timer_change
        
	return success_release_silver, timer_to_end


#######################################
#
# Main function to control the robot
# 
#######################################
def main():
    num_color_box = silver_box
    success_release = True
    success_grab = False
    timer_to_end = timer_end

    while timer_to_end >= 0:

        if num_color_box == silver_box and success_release:
		print("Looking for a silver box not already taken...")
		
		timer_to_end = timer_end
		success_grab, timer_to_end = grab_box(num_color_box, success_grab, timer_to_end)

		if success_grab:
			num_color_box = 1
			success_release = False

        if num_color_box == golden_box and success_grab:
		print("Looking for a golden box not already paired...")
		
		timer_to_end = timer_end
		success_release, timer_to_end = release_box(num_color_box, success_release, timer_to_end)

		if success_release:
			num_color_box = 0
			success_grab = False

    print("\nI've finished my work! All the boxes are paired... \nBye bye!")
    exit()


main()
