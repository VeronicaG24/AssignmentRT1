from __future__ import print_function

import time
from sr.robot import *

R = Robot()

list_token_silver = list()
list_token_gold = list()
color_token = [MARKER_TOKEN_SILVER, MARKER_TOKEN_GOLD]

a_th = 2.0
""" float: Threshold for the control of the orientation"""

d_th = 0.4
""" float: Threshold for the control of the linear distance"""

def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0


def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0


def find_token(col_num):
    """
    Function to find the closest silver token

    Returns:
	dist (float): distance of the closest token (-1 if no token is detected)
	rot_y (float): angle between the robot and the token (-1 if no token is detected)
    """
    dist=100
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
		
    if dist==100:
	return -1, -1, -1
    else:
   	return dist, rot_y, code
   	
   	
def main():
	step = 0
	success_release_gold = True
	success_release_silver = True
	success_grab_silver = False
	timer = 50
	timer_to_end = 30
	
	while(timer_to_end >= 0): 

		if step == 0 and success_release_silver: 
			print("step 0 - start")
			timer_to_end = 30
			while(not success_grab_silver and timer_to_end >= 0):
				if find_token(step)[0] == -1 or find_token(step)[1] == -1:
					turn(10, 1)
					print("I'm looking fo another box. Waiting util timer ends: " + str(timer_to_end))
					timer_to_end -= 1			
				elif find_token(step)[0] < d_th:
					list_token_silver.append(find_token(step)[2])
					print("codes of the silver box: " + str(list_token_silver))
					success_grab_silver = R.grab()
					timer = 50
				elif find_token(step)[1] > a_th:
					turn(1, 1)
					timer -= 1
				elif find_token(step)[1] < -a_th:
					turn(-1, 1)
					timer -= 1
				elif -a_th < find_token(step)[1] < a_th and find_token(step)[0] > d_th:
					drive(30, 1)
					timer -= 1
				
				if timer <= 0:
					print("I am not able to reach the box! I'll find another one")
					drive(-30,2)
					turn(40,2)
					timer = 50
					
			if(success_grab_silver):
				#drive(20, 3)
				#turn(10, 3)
				#success_release_silver = R.release()
				#if success_release_silver:
				step = 1
				success_release_silver = False
				#success_grab_gold = False
				#success_grab_silver = False
		
		if step == 1 and success_grab_silver:
			print("step 1 - start")
			timer_to_end = 30
			while(not success_release_silver and timer_to_end >= 0):
				if find_token(step)[0] == -1 or find_token(step)[1] == -1:
					turn(10, 1)
					print("I'm looking for another box. Searching util timer ends: " + str(timer_to_end))
					timer_to_end -= 1
				elif find_token(step)[0] < (d_th*2):
					list_token_gold.append(find_token(step)[2])
					print("codes of the golden box: " + str(list_token_gold))
					success_release_silver = R.release()
					drive(-10,3)
					timer = 50
				elif find_token(step)[1] > a_th:
					turn(1, 1)
					timer -= 1
				elif find_token(step)[1] < -a_th:
					turn(-1, 1)
					timer -= 1
				elif -a_th < find_token(step)[1] < a_th and find_token(step)[0] > d_th:
					drive(30, 1)
					timer -= 1
				
				if timer <= 0:
					print("I am not able to reach the box! I'll find another one")
					drive(-30,2)
					turn(40,2)
					timer = 50
					
			if(success_release_silver):
				#drive(20, 3)
				#turn(10, 3)
				#success_release_gold = R.release()
				#if success_release_gold:
				step = 0
				success_grab_silver = False
				#success_grab_gold = False
	
	print("I finished my work! Bye bye!")
	exit()		
	

main()
