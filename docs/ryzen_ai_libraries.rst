##################
Ryzen AI Libraries
##################

Users are expected to have minimal knowledge of installing Windows drivers and C++ programming in Windows development.  After reading this document, users should be able to setup and use CVML SDK samples following the steps outlined.

The latest iteration of the CVML SDK contains the following features:

- Auto framing
- Depth Estimation
- Eye Gaze Correction
- Face Detection
- Human Segmentation
- LowLight Denoiser
- Super Resolution

HARDWARE & SOFTWARE REQUIREMENTS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

AMD HARDWARE REQUIREMENTS
#########################

The CVML SDK is intended to work with the following AMD device(s): Phoenix

CVML SDK works with any camera connected with the computer (USB or integrated). CVML SDK supports 720p or 1080p resolutions. We recommend using Logitech C920 PRO HD Webcam or Logitech BRIO Webcam as our development teams use them for reference.  

PREREQUISITE SOFTWARE PACKAGES
##############################

Download the required software packages below to build and run CVML SDK applications. Ensure that they are added to the Path environment variable. Path can be tested by running the executables in command prompt. Download Windows packages.

Table 1: Software Prerequisites


PROGRAMMING GUIDE
~~~~~~~~~~~~~~~~~

API DOCUMENTATION
#################
Detailed API documentation is available in Doxygen format

FEATURE HEADER REQUIREMENTS
###########################
The API headers are packaged into a single folder and are meant to be included (depending on what functions are needed from the CVML SDK) as part of the compilation. Table 2 outlines the minimum header files required for each feature respectively. The section API Include Headers lists all the available included headers with a brief description.




FEATURE DYNAMIC LIBRARY REQUIREMENTS
####################################

There are core and feature specific dynamic libraries. This allows for modularization of the required DLLs for the desired feature(s). The full list of libraries and their descriptions are in the Dynamic Libraries section of the Appendix.

The path environment variable to the CVML SDK lib folder must be established to run the features. This can be done using a command prompt with the following command:

.. code-block::

   set PATH=%PATH%;%CVML_SDK_LIB_PATH%

Close the command prompt after this step to reflect the change to the PATH variable.

PROGRAMMING FLOW
################


Figure 1: General programming sequence of CVML SDK features
A CVML context is necessary to use the CVML features.
Feature(s) will then use the pointer to the CVML context to create an instance.
The API will check if the feature(s) are supported on the current platform and allocate acceleration engines depending on the utilization of the system before building the feature.
Preprocess the format of the frame/image to be in RGB before executing the built feature(s). After execution, the feature(s) will return the result(s) from the inference. This entire step is done in a loop for as long as the feature is enabled and running.
Release the CVML context to undo the allocation of both the CVML context as well as the feature(s).

BUILDING AND RUNNING CVML SDK SAMPLES
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Besides the provided prebuilt sample executables, users can also follow below instructions to build executables from altered samples.

ADD LIB TO PATH
###############
Open command prompt and add SDK lib folder to PATH variable.

set PATH=%PATH%;%CVML_SDK_LIB_PATH%

Close the command prompt after this step to reflect the change to the PATH variable.

CONFIGURE CMAKELISTS.TXT
########################
In samples/CMakeLists.txt line 12, change example path for OPENCV_INSTALL_ROOT to location of the OpenCV install build folder (i.e. C:/**/opencv/build)

  11 # Please set opencv install root path, below is an example
12 set(OPENCV_INSTALL_ROOT "C:/cvml/tools/opencv/build")
    
Note: Sample apps use opencv library. Please make sure OpenCV_DIR in related CMakeList.txt file is properly set as per the opencv installed path in the build environment.

Note msvc-142 is equivalent to VS2019

BUILDING SDK SAMPLES
####################
Open command prompt and change directory to samples folder.  Run ms-build-samples.bat.

If the build is successful, last console output will “be >exit /b 0”. See Figure 2 for correct output after a successful build.



Figure 2: ms-build-samples.bat correct output
A new folder named build-samples will be created within the samples folder of the SDK. Refer to Figure 3



Figure 3: Built Samples Folder

IPU DRIVER SETUP AND RADEON ML DEVELOPMENT
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Development directly using the Radeon ML and IPU driver setup can be found in in the “PHX IPU Driver Setup User Guide for 0.8.5.1.pdf"

APPENDIX
~~~~~~~~

FILE CONTENTS
#############
The CVML SDK is packaged as a ZIP file.  Extract using 7-zip or similar decompression tool.

API INCLUDE HEADERS
###################
Table 3: Header Descriptions
Header File

Header Type and Description

cvml-api-common.h

core header containing API required by each feature

cvml-auto-framing.h

header containing CVML auto framing feature API

cvml-context.h

core header containing CVML context and context builder API

cvml-image.h

core header containing CVML image API

cvml-logger.h

core header containing CVML SDK logging interface

cvml-face-detector.h

header containing CVML face detection feature API

cvml-eyegaze-correction.h

header containing CVML eye gaze correction feature API

cvml-depth-estimation.h

header containing CVML depth estimation feature API

cvml-super-resolution.h

header containing CVML super resolution feature API

cvml-lowlight-denoiser.h

header containing CVML lowlight denoiser feature API

cvml-scene-detection.h

header containing CVML scene detection feature API

cvml-human-segmentation.h

header containing CVML human segmentation feature API

float16.hpp

header containing API to support floating point 16

DYNAMIC LIBRARIES
#################

The SDK is structured with 2 levels of APIs from code modularization perspective. A set of core libraries that are needed for every CVML feature and a set of libraries which are feature specific. This allows applications to incorporate only the core and sub-set of features that are of interest. Table 4 describes CVML SDK library binaries calling relationship:

Table 4: SDK Lib Binary Descriptions
Library Binary

Core or Feature Library and Description

amdblitter.dll / amdblitter.cl.bin

Core library for image processing used during model pre-process and post-processing

cvml-*.dll

Core SDK and feature libraries

tvm_runtime.dll

Core library for TVM run time to load feature model

*.amodel

Inference data for each feature

SAMPLE FILES
############
A precompiled binary and its corresponding sources are available for developers to use as a reference during integration. Edited sample source code can be built running ms-build-samples.bat.

FREQUENTLY ASKED QUESTIONS
##########################
When running the sample executables, I get a opencv_world*.dll was not found error:


Need to add OpenCV lib folder to path: set PATH=%PATH%; %OPENCV_PATH%

When running the sample executables, I get a cvml-sdk.dll was not found error:


Need to add lib folder to path: set PATH=%PATH%; %CVML_SDK_LIB_PATH%


..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.

