cmake -B build -S . -DCMAKE_TOOLCHAIN_FILE=C:/Users/elelm/vcpkg/scripts/buildsystems/vcpkg.cmake
cmake --build .\build\    

.\build\Debug\BlinkProg.exe   

cmake -B build -S . -DCMAKE_TOOLCHAIN_FILE=/Users/hansivarolberg/vcpkg/scripts/buildsystems/vcpkg.cmake

vcpkg install liblsl
vcpkg install crow