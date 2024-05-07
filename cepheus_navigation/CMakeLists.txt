cmake_minimum_required(VERSION 3.0.2)
project(cepheus_navigation)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  message_generation
  std_srvs
)

add_service_files(
  FILES
  Checkpoint.srv
)

generate_messages(
  DEPENDENCIES
)

catkin_package(
  CATKIN_DEPENDS message_runtime
  )

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)
