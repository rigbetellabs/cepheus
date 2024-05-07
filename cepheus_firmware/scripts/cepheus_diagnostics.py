#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int32
import time

def publish_integer():
    # Initialize the ROS node
    rospy.init_node('diagnostics test', anonymous=True)

    # Create a publisher for the /test topic with Int32 type
    pub = rospy.Publisher('/diagnostics/test', Int32, queue_size=10)

    # Define prompts for each input value
    prompts = {
#        0: "Do you want to run full diagnos test? (y/n): ",
        1: "Running motor and encoder connections/diagnostics test, Please confirm your robot is uplifted and emergency switch is open (y/n): ",
        2: "Do you want to run motor direction test? (y/n): ",
        3: "Do you want to run IMU connections/diagnostics test? (y/n): ",
        4: "Do you want to run display connection/diagnostics test? (y/n): ",
        5: "Do you want to publish 5? (y/n): ",
        6: "Do you want to publish 6? (y/n): ",
        7: "Do you want to publish 6? (y/n): "
    }
    print("")
    print("")
    print("Cepheus diagnostics test")
    print("")
    print(" *******************************************")
    print("")
    print(" 0: To run full diagnos test ")
    print(" 1: To run Motor and encoder connections/diagnostics test ")
    print(" 2: To run motor direction test ")
    print(" 3: To run IMU connections/diagnostics test ")
    print(" 4: To run display connection/diagnostics test ")
    # print("5: Do you want to publish 5? (y/n): ")
    # print("6: Do you want to publish 6? (y/n): ")
    # print("7: Do you want to publish 6? (y/n): ")
    print("")
    print(" *******************************************")
    print("Enter test code and press Enter.")
    print("Press Ctrl+C to exit.")
    print("")

    # Run the loop to continuously prompt the user for an integer input
    while not rospy.is_shutdown():
        try:
            user_input = int(input("Enter test code: "))
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
            continue

        if user_input < 0 or user_input > 7:
            print("Input must be between 0 and 7.")
            continue

        confirmation = input(prompts[user_input]).lower()
        if confirmation == 'y' or confirmation == '':

            if user_input == 2:
                
               # Robot forward direction test
               print(" ")
               print("Robot forward test: make sure robot is moving forward and all wheels rotate in forward direction");
               feed_input = input("Are you ready to move forward? (y/n)".lower())
               if feed_input == 'y' or feed_input == '':
                   pub.publish(21)
                   time.sleep(5)
                   feed_input = input("is robot/all motors moving forward? (y/n)".lower())
                   if feed_input == 'y' or feed_input == '':
                       print("*** Great!! now ready for backward test ***")
                       #publish forward diagnos result here
                   else:
                    print("Robot forward test: Failed")
                    #publish forward diagnos result here
                    continue
                
                # Robot backward direction test  
               print(" ");
               print("Robot backward test: make sure robot is moving backward and all wheels run in backward direction"); 
               #time.sleep(3)
               feed_input = input("Are you ready to move backward? (y/n)".lower())
               if feed_input == 'y' or feed_input == '':
                   pub.publish(22)
                   time.sleep(5)
                   feed_input = input("is robot/all motors moving backward? (y/n)".lower())
                   if feed_input == 'y' or feed_input == '':
                       print("*** Great!! now ready for turing left test ***")
                       #publish backward diagnos result here
                   else:
                    print("Robot backward test: Failed")
                    #publish backward diagnos result here
                    continue
                
               # Robot left direction test  
               print(" ");
               print("Robot rotate left test: make sure robot is moving towards left direction and left wheels moving backward and right wheels moving to forward direction"); 
               #time.sleep(3)
               feed_input = input("Are you ready to rotate robot in left direction? (y/n)".lower())
               if feed_input == 'y' or feed_input == '':
                   pub.publish(23)
                   time.sleep(5)
                   feed_input = input("is robot rotate to left direction? (y/n)".lower())
                   if feed_input == 'y' or feed_input == '':
                       print("*** Great!! now ready for right turing test ***")
                       #publish left rotate diagnos result here
                   else:
                    print("Robot rotate left test: Failed")
                    #publish left rotete diagnos result here
                    continue
                
               # Robot right direction test  
               print(" ")
               print("Robot rotate right test: make sure robot is moving towards right direction and right wheels moving backward and left wheels moving forward direction"); 
               #time.sleep(3)
               feed_input = input("Are you ready to rotate robot in right direction? (y/n)".lower())
               if feed_input == 'y' or feed_input == '':
                   pub.publish(24)
                   time.sleep(5)
                   feed_input = input("is robot rotate to right direction? (y/n)".lower())
                   if feed_input == 'y' or feed_input == '':
                       print("*** Great!! now ready for linear left movement test ***")
                       #publish right rotate diagnos result here
                   else:
                    print("Robot rotate right test: Failed")
                    #publish right rotete diagnos result here
                    continue
                
               # Robot linear left movement test  
               print(" ");
               print("Robot linear left movement test: make sure robot is moving towards linear left direction (on Y axis) "); 
               #time.sleep(3)
               feed_input = input("Are you ready to move robot in linear left direction (Y axis)? (y/n)".lower())
               if feed_input == 'y' or feed_input == '':
                   pub.publish(25)
                   time.sleep(5)
                   feed_input = input("is robot move towards linear left (Y axis) direction? (y/n)".lower())
                   if feed_input == 'y' or feed_input == '':
                       print("*** Great!! now ready for linear right movement test ***")
                       #publish linear left move diagnos result here
                   else:
                    print("Robot linear left movement test: Failed")
                    #publish linear left move diagnos result here
                    continue
                
               # Robot linear right movement test  
               print(" ");
               print("Robot linear right movement test: make sure robot is moving towards linear right direction (on Y axis) "); 
               #time.sleep(3)
               feed_input = input("Are you ready to move robot in linear right direction (Y axis)? (y/n)".lower())
               if feed_input == 'y' or feed_input == '':
                   pub.publish(26)
                   time.sleep(5)
                   feed_input = input("is robot move towards linear right (Y axis) direction? (y/n)".lower())
                   if feed_input == 'y' or feed_input == '':
                       print("*** Great!! all test completed ***")
                       #publish linear rihgt move diagnos result here
                   else:
                    print("Robot linear right movement test: Failed")
                    #publish  linear right move diagnos result here
                    continue
                               
               else:
                   print("Motor Direction test : aborted!!")
                   
            # Publish the user input to the /test topic
            else:
                pub.publish(user_input)
        else:
            print("Publishing canceled.")

if __name__ == '__main__':
    try:
        publish_integer()
    except rospy.ROSInterruptException:
        pass
