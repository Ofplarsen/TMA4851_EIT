## Tutorial

### Install vcpkg
https://vcpkg.io/en/getting-started

#### Install
- sudo ./vcpkg install liblsl
- sudo ./vcpkg install asio
- sudo ./vcpkg install pugixml

### Build
- cmake -B build/ -S . -DCMAKE_TOOLCHAIN_FILE=/dev/vcpkg/scripts/buildsystems/vcpkg.cmake && cmake --build build/ && ./build/main 
- cmake -B [build directory] -S . -DCMAKE_TOOLCHAIN_FILE=[path to vcpkg]/scripts/buildsystems/vcpkg.cmake 
- cmake --build [build directory]
