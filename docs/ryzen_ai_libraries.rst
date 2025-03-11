.. Copyright (C) 2023 Advanced Micro Devices, Inc. All rights reserved.

##############################################
Getting started with Ryzen AI Library features
##############################################

The Ryzen AI Libraies build on top of the Ryzen AI drivers and execution infrastructure to provide powerful AI capabilities to C++ applications without having to worry about training specific AI models and integrating them to the Ryzen AI framework.

Each Ryzen AI library feature offers a simple C++ application programming interface (API) that can be easily incorporated into existing applications.

*************
Prerequisites
*************
Ensure that the following software tools/packages are installed on the development system.

  1. Visual Studio 2022 Community edition or newer, ensure “Desktop Development with C++” is installed
  2. Cmake (version >= 3.18)
  3. OpenCV (version=4.8.1 or newer)

*********************************************
Building Ryzen AI Library sample applications
*********************************************
This section covers the steps to build all sample applications.

Navigate to the folder containing Ryzen AI samples
==================================================
Go to the 'samples' sub-folder of the Ryzen AI Library. ::
  
  chdir samples

Specify location of OpenCV libraries
====================================
Ryzen AI Library samples make use of OpenCV, so set an environment variable to let the build scripts know where to find OpenCV. ::

  set OPENCV_INSTALL_ROOT=<location of OpenCV libraries>

Build the sample applications
=============================
Create a build folder and use CMAKE to build the sample(s). ::

  mkdir build-samples
  cmake -S %CD% -B %CD%\build-samples -DOPENCV_INSTALL_ROOT=%OPENCV_INSTALL_ROOT%
  cmake --build %CD%\build-samples --config Release

The compiled sample application(s) will be placed in the various build-samples\<application>\Release folder(s) under the 'samples' folder.

*********************************************
Running Ryzen AI Library sample applications
*********************************************
This section describes how to execute Ryzen AI Library sample applications.

Update the console and/or system PATH
=====================================
Ryzen AI Library applications need to be able to find the library files. One way to do this is to add the location of the libraries to the system or console PATH environment variable.

Additionally, the location of OpenCV's runtime libraries needs to be added to the PATH environment variable. ::

  set PATH=%PATH%;<location of Ryzen AI Library package>\windows
  set PATH=%PATH%;%OPENCV_INSTALL_ROOT%\x64\vc16\bin

Adjust the aforementioned commands to match the actual location of Ryzen AI and OpenCV libraries, respectively.

Select an input source/image/video
==================================
Ryzen AI Library samples can accept a variety of image and video input formats, or even open the default camera on the system if "0" is specified as an input.

In this example, a publically available video file is used for the application's input. ::

  curl -o dancing.mp4 https://videos.pexels.com/video-files/4540332/4540332-hd_1920_1080_25fps.mp4

Execute the sample application
==============================
Finally, the previously built sample application can be executed with the selected input source. ::

  build-samples\cvml-sample-depth-estimation\Release\cvml-sample-depth-estimation.exe -i dancing.mp4
..
  ------------

  #####################################
  License
  #####################################

  Ryzen AI is licensed under MIT License. Refer to the LICENSE file for the full license text and copyright notice.
