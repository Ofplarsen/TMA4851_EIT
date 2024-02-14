# Minimum version of CMake required to build this project
cmake_minimum_required(VERSION 3.0)

# Name of the project
project(BlinkProg)

find_package(Crow CONFIG REQUIRED)
find_package(Boost REQUIRED COMPONENTS system)
# Add a library to this build. The name of the library is MyLibrary and it
# consists of only the MyLibrary.cpp file
add_executable(BlinkProg blink.cpp)
include_directories(${Boost_INCLUDE_DIRS})
target_link_libraries(BlinkProg PUBLIC Crow::Crow)
