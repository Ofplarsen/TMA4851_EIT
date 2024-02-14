cmake_minimum_required(VERSION 3.0)
project(LSLTest)

# Set C++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)
find_package(SDL2 REQUIRED)
find_package(LSL CONFIG REQUIRED)
find_package(asio CONFIG REQUIRED)
find_package(pugixml CONFIG REQUIRED)
find_package(Boost REQUIRED COMPONENTS system)
include_directories( ${CURSES_INCLUDE_DIRS} )
include_directories(${SDL2_INCLUDE_DIRS})
include_directories(${Boost_INCLUDE_DIRS}) 

function(addlslexample name extension)
	add_executable(${name}
		${name}.${extension}
	)
	target_link_libraries(${name} PRIVATE LSL::lsl)
	#target_link_libraries(${name} PRIVATE asio::asio)
	#target_link_libraries(${name} PRIVATE pugixml::static pugixml::pugixml)
	target_link_libraries(${name} PRIVATE ${SDL2_LIBRARIES})
	target_compile_features(${name} PRIVATE cxx_constexpr)
	installLSLApp(${name})
endfunction()

addlslexample(main cpp)
find_package(Threads)
