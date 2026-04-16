# RoboticsA2
# Automated Bin Transportation Robot 

## 1.	Project overview 
This project focuses on the design and development of an automated robot capable of transporting bins from one location to another. The system uses a VEX EXP robot combined with programmed control logic to simulate a real-world industrial task. 

The aim of the project is to demonstrate how robotics can be used to automate repetitive tasks such as moving items in environments like warehouses, manufacturing and logistics. The robot is designed to move towards an object, pick it up using a claw mechanism, and transport it to a designated location.

This project highlights how automation can improve efficiency, reduce human effort, and increase consistency in repetitive processes. This system focuses on physical and programmed control logic to automate a repetitive transport task. A raspberry Pi vision subsystem was alos explored during development as a possible extention. 

# 2.	Problem being solved 
In environments such as warehouses and factories, moving items manually can be physically demanding, inefficient, and time-consuming. When large numbers of items or containers need to be relocated, human involvement can slow processes down and increase labour costs.

This project addresses this issue by creating a robotic system that can:
- move towards a bin
- secure it using a claw mechanism
- transport it to a new location
- release it accurately

This improves efficiency and reduces the need for manual handling. 

# 3.	Hardware used 
The hardware used in this project includes:
- VEX EXP Robot
- Left and right drive motors (for movement)
- Arm motor (for lifting the bin)
- Claw motor (for gripping the bin)
- Raspberry Pi
- Raspberry Pi Camera Module 2
- Inertial sensor 

The final demonstrated system uses VEX EXP robot, its drive motors, arm motor, claw mtotr and inertial sensor to complete the task automatically. A Raspberry Pi and camera module were also explored during development as an extention for visual sensing. 

# 4.	Software used 
The software used in this project includes:
- VEXcode Python - used to program the robot
- Thonny (Raspberry Pi IDE) - used to run Python scripts on the Raspberry Pi
- Python programming language for implementing control logic
- Basic image processing techniques for handling camera input

The final demonstrated solution runs on the VEX EXP robot using VEXcode Python. Seperate Pi camera code was also developed during the project as an extention.

# 5.	Control algorithm 
The robot follows a step-by-step control algorithm to complete the task:
1. Calibrate the inertial sensor
2. Move the arm to the start position
3. Open the claw
4. Move to the pickup point
5. Close the claw to grip the bin
6. Reverse slightly and lift the arm
7. Return to the home position
8. Turn towards the correct drop-off location
9. Move to the drop-off point
10. Open claw to release the bin
11. Reverse back to home
12. Repeat for remaining items 

This algorithm uses programmed robot movement and inerial-senor-based heading control to perform the task automatically in a controlled enviornment.

# 6.	How to run the code 
1. Open the robot program in VEXcode Python
2. Connect the VEX EXP brain to VEXcode
3. Upload the program to the robot
4. Place the robot in home position
5. Place the items pickup points A, B and C.
6. Run the program

This robot will automatically collect each item, transport it to its assigned drop-off point.

# 7. System behaviour
The final demonstration works through programmed movement and co-ordinated motor control. The robot follows a fixed sequence to approach each pickup point, grip the item, lift it, transport it to the correct drop-off location, release it and return home.
The inertial sensor is used to improve accuracy and help the robot maintain its heading during the task.

A Raspberry Pi camera subsystem was explored during development as a possible extdention, but it was not included in the final live demonstration. 
# 8. Limitations 
There are some limitations within the system: 
- The robot follows pre-defined movements and does not dynamically adjust its path
- There is no obstacle avoidance 
- The system assumes the bin is placed within a known position
- The system works best in a controlled environment
- A Raspberry Pi camera subsystem was explored during development, but it was not included in the final live demonstration.
These limitations mean the system works best in a controlled environment.

# 9. Possible improvements 
- Implement obstacle detection using sensors
- Fully integrate a vision subsystem for colour-based object identification 
- Add dynamic navigation instead of fixed movements
- Allow the robot to handle multiple bins automatically

These improvements would make the system more efficient and closer to real-world industrial robotics. 

# 10. References 
- VEX Robotics
- Raspberry Pi Documentation
- Python Documentation
- Lecture materials and workshop content

# 11. AI Transparcy Statement 
AITS 3 - AI has been used for development: During the early phase, AI tools were used to help generate ideas, refine the project concept, and outline the structure of the sorting robot system. AI also assisted in problem-solving throughout the design process. For example, it provided guidance on programming logic. This helped with the development process and reduced the time spent troubleshooting issues.
