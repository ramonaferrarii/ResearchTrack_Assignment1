# ResearchTrack_Assignment1
This is a report for the first assignment of the Research Track course, for the *Robotics Engineering Master's degree* at the University of Genoa.

## Simulator
This is a simple, portable robot simulator developed by Student Robotics. The simulator requires a Python 2.7 installation, the pygame library, PyPyBox2D, and PyYAML. The simulator shows a space where a robot can move and interact with tokens. In general tokens can be gold or silver. In this specific case, we have only gold tokens. Other important information are in the `README` of the branch assignment23. 

## Run the code
The steps to run the code are the following:
1) Clone the repository
2) Move into the branch with the command `git checkout assignment23`
3) Enter in the folder which contains the file `assignment.py`
4) Launch the program with the command `python2 run.py assignment.py`

# Assignment
Write a python node that controls the robot to put all the golden boxes together. 

## At the beginning 
Firstly, the robot is in the upper left corner and it sees only front of it. There are 6 tokens, placed along a circle. 
Notice the code does not depend on the number of tokens.

## Description of the code in few words
The idea of this code is to allow the robot to see all tokens, pick them up one by one and take them to a previous choosen destination (in this case, the position of the last token seen). 

## Pseudocode
Before starting with python code, it has been fundamental writing the pseudocode to clarify the steps to follow:
```python
function main():
  # Robot sees tokens
  initialization of the robot and parameters (thresholds)
  for i in range(24)
    robot turns and sees tokens
    token_info = tokens seen
    return token_info

  # Choice of the destination  
  sort tokens by distance
  destination_token = last token of token_info
 
  # Robot moves to grab the token
  while(there are tokens to collect)
    first = firt token of token_info
    while(token is not Visible)
      turn
     
    while( robot does not reach it)
      turn/drive and update dist and rot_y

    grab the token

    # Robot moves to release the token
    while(destination is not Visible)
      turn/drive and update dist and rot_y

    release the token
```

# Global variables:
`d_th` and `a_th` are respectively the thresholds used to adjust the motion of the robot.

## Description of the functions used:
### Functions already implemented:
`turn`: it sets the angular velocity of the robot, using two parameters, speed and time.
`drive`: it sets the linear velocity of the robot, using two parameters, speed and time.

### New functions: 
`find_all_tokens`: it allows the robot to rotate approximately 360 degrees. During scanning, the robot sees the tokens and stores their identifier (code), distance (dist), and rotation around the Y-axis (rot_y) in a list of tuples, named token_info. 

`rotate_into_visibility`: it takes token_info as parameter. It allows to position the robot allowing it to see the token considered. It has no return.

`get_dist_and_rot`: it takes token_code and care_about_size as parameter and it is necessary to update the position of the robot, during its motion.

`move to token`: it takes token_code and care_about_size as parameter. This function works when the robot is going to grab the token and also when robot is taking a token to destination. care_about_size is n when the the robot is moving towards to destination (to avoid the collision with the "destination token"), otherwise it is 0. n increases every time the robot considers another token: more tokens there are, further the token we are carrying will be placed from the destination. 

## Further improvements
 1) By adjusting the speed of the turn function, it is possible to achieve smoother motion.
 2) To prevent collisions between the token and the robot, it is advisable to reduce the time taken for the drive function. In general, the objective is to find a balance between speed/time and motion accuracy.
 3) Another effective solution to avoid collisions is to implement a function that dynamically changes the destination to the nearest token whenever the robot moves towards its destination, or a function that intelligently avoids obstacles.
 4) The destination is currently fixed and determined as the last token detected by the find_all_tokens function. Instead, the choice could be made randomly or by computing the midpoint between the nearest and farthest tokens and setting that point as the destination.
 5) While this algorithm is quite versatile and suitable for any token position, it may not be the most efficient if the positions of the tokens are precisely known and follow a specific structure.

Nevertheless, despite possible modifications, the developed code adequately fulfills the requirements in a general manner, while aiming to make minimal assumptions.




