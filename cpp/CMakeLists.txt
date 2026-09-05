cmake_minimum_required(VERSION 3.20)
project(sotto_demo LANGUAGES CXX)

add_executable(demo main.cpp)
target_compile_features(demo PRIVATE cxx_std_17)
# Keep the executable in build/ with both single- and multi-config generators.
set_target_properties(demo PROPERTIES RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/$<0:>")
