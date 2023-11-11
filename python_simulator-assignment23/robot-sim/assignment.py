from __future__ import print_function

import time
from sr.robot import *

""" 
    To run the code:
    $ python run.py assignment.py
"""


a_th = 2.0
""" float: Threshold for the control of the orientation"""

d_th = 0.4
""" float: Threshold for the control of the linear distance"""

R = Robot()


# Functions to move the robot
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
    

# Function to count how many tokens there are
def find_all_tokens():
    seen_tokens = {}
    token_info = []

    # The robot turns about 360 degrees 
    for i in range(24):
        turn(50, 0.1)
        time.sleep(0.1)
        marker_info = R.see()
        
        # Check if the token has already be seen
        for marker in marker_info:
            marker_code = marker.info.code

            if marker_code in seen_tokens:
                continue
            
            seen_tokens[marker_code] = marker.centre.polar.rot_y
            token_info.append((marker_code, marker.dist, marker.rot_y))     # it's possible to not consider rot_y since it's useless
            

    # Print of what the robot sees and the info (code, dist and rot_y) about each token
    print("Total distinct tokens seen:", len(seen_tokens))
    print("Token info:")
    for token_code, dist, rot_y in token_info:
        print("Token code:", token_code, "Distance:", dist, "Rot_y:", rot_y)

    return token_info   
    


# Function to check if the token is still visibile by the robot
def rotate_into_visibility(token_code):
    isVisible = False
    # Robot tuns until the token is visible
    while(not isVisible):
        turn(30, 0.1)
        visible_codes = [marker.info.code for marker in R.see()]
        if token_code in visible_codes:
            isVisible = True
            
            
# Function to get distance and rot_y of tokens
def get_dist_and_rot(token_code, care_about_size):
    dist = 0
    rot_y = 0
    found = False
    for marker in R.see():
        if marker.info.code == token_code:          
            dist = marker.dist - marker.info.size * care_about_size
            rot_y = marker.rot_y
            found = True
            break # when the robot finds the token, its info are saved 

    return dist, rot_y, found


def move_to_token(token_code, care_about_size=0):
     
    # Now we know that closest is currently visible
    found = False
    while not found:
        rotate_into_visibility(token_code)
        dist, rot_y, found = get_dist_and_rot(token_code, 0)
    
    # Robot moves until it reaches the token
    while dist > d_th or abs(rot_y) > a_th:
        #print(dist, " ", rot_y)    # debug print

        if rot_y > a_th:
            turn(10, 0.1)
        elif rot_y < -a_th:
            turn(-10, 0.1)
        else:
            drive(100, 0.01)

        dist, rot_y, found = get_dist_and_rot(token_code, care_about_size)
        while not found:
            rotate_into_visibility(token_code)
            dist, rot_y, found = get_dist_and_rot(token_code, care_about_size)

    

def main():
    token_info = find_all_tokens()

    token_info.sort(key=lambda k: k[1]) # sort token info in place, by distance from robot (in order to get the current minimum easily)

    destination_token = token_info.pop(len(token_info) - 1) # choice of the destination of all boxes
    n = 1 # it changes every time to try to avoid collision between robot and token
    
    # Collect tokens
    while len(token_info) > 0:
        first = token_info.pop(0)  # first = (id, dist, -rot_y-); remember rot_y is useless
        # Robot moves towards to the token; it does not care about token's size because it wants to grab it
        move_to_token(first[0])
        R.grab()
        print("Got a token!")
        # Robot moves towards to destination and cares about token's size to avoid collision
        move_to_token(destination_token[0], care_about_size=n)  
        R.release()
        drive(-50, 0.5)
        n += 0.8 

    print("All tokens collected!")

main()	
	
	


