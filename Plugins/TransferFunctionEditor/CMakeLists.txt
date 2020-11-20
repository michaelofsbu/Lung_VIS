cmake_minimum_required(VERSION 3.1 FATAL_ERROR)

project(TransferFunctionEditor CXX)

set(CMAKE_INCLUDE_CURRENT_DIR ON)
set(CMAKE_AUTOMOC ON)

find_package(Qt5 COMPONENTS Core Gui OpenGL Widgets REQUIRED)
# Let QT pre-process the files and add the generated files to the source list
#qt5_wrap_ui(GENERATED_SOURCES ${GRAPHICS_UIS})
source_group("Generated Sources - Do Not Edit" FILES ${GENERATED_SOURCES}) 

# Make sure the compiler can find the pre-processed files from qt4_wrap_ui
include_directories(${CMAKE_CURRENT_SOURCE_DIR})
include_directories("${CMAKE_BINARY_DIR}")
include_directories("${PROJECT_SOURCE_DIR}")
include_directories("${PROJECT_BINARY_DIR}")
include_directories("${PROJECT_SOURCE_DIR}/..")

find_package(VTK REQUIRED)

set(TFE_SOURCES
    vpDbsRect.cpp
    vpDbsRect.h
    vpDoubleSlider.cpp
    vpDoubleSlider.h
    vpDragableEnd.cpp
    vpDragableEnd.h
    vpTFNode.h
    vpTFNode.cpp
    vpTFNode.h
    vpTFQuad.cpp
    vpTFQuad.h
    vpTFScene.cpp
    vpTFScene.h
    vpTransferFunction.cpp
    vpTransferFunction.h
    vpTransferFunctionEditor.cpp
    vpTransferFunctionEditor.h
)

add_library(TransferFunctionEditor SHARED ${TFE_SOURCES})
 
target_link_libraries(TransferFunctionEditor
    Qt5::Core Qt5::Widgets Qt5::OpenGL Qt5::Gui
    ${VTK_LIBRARIES} 
)

target_include_directories(TransferFunctionEditor PUBLIC
    ${PROJECT_SOURCE_DIR}
)
