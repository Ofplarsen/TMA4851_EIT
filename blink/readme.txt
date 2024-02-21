cmake -B build -S . -DCMAKE_TOOLCHAIN_FILE=C:/Users/elelm/vcpkg/scripts/buildsystems/vcpkg.cmake
// If not work, delete build folder.

cmake --build .\build\    
.\build\Debug\BlinkProg.exe   