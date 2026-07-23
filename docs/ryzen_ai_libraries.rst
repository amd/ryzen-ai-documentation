.. Copyright (C) 2023-2026 Advanced Micro Devices, Inc. All rights reserved.

#####################
Ryzen AI CVML library
#####################

The Ryzen AI Libraries build on top of the Ryzen AI drivers and execution
infrastructure to provide powerful AI capabilities to C++ applications without
having to worry about training specific AI models and integrating them to the
Ryzen AI framework.

Each Ryzen AI CVML library feature offers a simple C++ application programming
interface (API) that can be easily incorporated into existing applications.

.. contents:: Table of Contents
   :local:
   :depth: 2

*****************
Package Contents
*****************

The Ryzen AI CVML library consists of the following files and folders:

- **cmake/** — Packaging info for CMake's find_package function
- **include/** — C++ header files
- **windows/** — Binary files for Windows, including both compile time .LIB files and runtime .DLL/.GRAPHLIB/.AMODEL files
- **linux/** — Binary files for Linux, including compile and runtime .SO files
- **samples/** — Individual sample applications
- **LICENSE.txt** — License file

*****************************************************
Executing Ryzen AI CVML library enabled applications
*****************************************************

The Ryzen AI CVML library selects the appropriate hardware (for example GPU or NPU) and framework for performing inference operations by default. An API is also available to set the preferred inference backend for those applications that wish to do so.

In order to execute applications that utilize the Ryzen AI CVML library, the appropriate drivers must first be installed on the target system, and the Ryzen AI CVML library files must be included with the application itself.

.. note::

 Ryzen AI CVML library features that utilize the ONNX backend for NPU operations might experience a longer startup latency the first time they are executed on a device. This increased startup latency does not occur for subsequent runs of the feature.

.. note::

   If the NPU driver is not installed on the target system, the Ryzen AI CVML library will automatically fall back to the GPU backend for inference operations.

.. _dependencies:

Prerequisites and dependencies
================================

The AMD Adrenalin and Ryzen AI drivers should be installed before attempting to execute Ryzen AI CVML library applications.

Download Ryzen AI CVML Library package
---------------------------------------

Create an AMD account at `account.amd.com <https://account.amd.com>`_ if you don't have one, then sign in to download the Ryzen AI CVML Library from the AMD Account Portal: ::

  https://account.amd.com/en/forms/downloads/xef.html?filename=72293_Ryzen_AI_Library_26.07.15.zip

After downloading, extract the package to a local directory (e.g., ``C:\RyzenAI-Library`` on Windows or ``~/RyzenAI-Library`` on Linux) and set the ``AMD_CVML_SDK_ROOT`` environment variable to the extracted location.
s
.. _windows_setup:

Windows Setup
==============

The following installations are for Windows OS. For Linux OS, follow `Ubuntu Setup`_ instructions.

AMD Adrenalin driver
---------------------

Install either the following Adrenalin driver or a newer one: https://www.amd.com/en/support/download/drivers.html

AMD Ryzen AI driver
--------------------

Install the latest Ryzen AI NPU driver from https://ryzenai.docs.amd.com/en/latest/inst.html

Version 32.0.203.280 or newer is required; both listed versions (32.0.203.280 and 32.0.203.314) are compatible.

OpenCV
-------

Download the OpenCV 4.11 Windows installer from the GitHub releases page: https://github.com/opencv/opencv/releases/tag/4.11.0

Download ``opencv-4.11.0-windows.exe``, run it, and extract to a local folder (e.g. ``C:\opencv``). The ``build`` subfolder (e.g. ``C:\opencv\build``) contains ``OpenCVConfig.cmake`` and is the path to use for ``OPENCV_INSTALL_ROOT``.

.. _linux_setup:

Ubuntu Setup
=============

The following installations are for Ubuntu. For Windows OS, follow `Windows Setup`_ instructions.

Ensure that the following software tools/packages are installed on the development system:

1. OS: Ubuntu 22.04 or Ubuntu 24.04 (linux kernel >= 6.11.0-21-generic)
2. Install latest Ryzen AI NPU driver following the "`Install NPU Drivers <https://ryzenai.docs.amd.com/en/latest/linux.html>`_" section
3. Vulkan SDK
4. OpenCV 4.11.0 — build from source following the instructions in ``README-linux.md``

Installing VulkanSDK and 22.04/24.04 specific installs
--------------------------------------------------------

::

  UBUNTU_CODENAME=$(. /etc/os-release; echo "$UBUNTU_CODENAME")
  wget -qO- https://packages.lunarg.com/lunarg-signing-key-pub.asc | sudo tee /etc/apt/trusted.gpg.d/lunarg.asc
  sudo wget -qO /etc/apt/sources.list.d/lunarg-vulkan-1.3.296-$UBUNTU_CODENAME.list https://packages.lunarg.com/vulkan/1.3.296/lunarg-vulkan-1.3.296-$UBUNTU_CODENAME.list
  sudo apt update
  sudo apt install vulkan-sdk

Additional installation for Ubuntu 22.04: Update MESA Vulkan Drivers
----------------------------------------------------------------------

::

  sudo apt update && sudo apt upgrade
  sudo add-apt-repository ppa:kisak/kisak-mesa -y
  sudo apt update
  sudo apt upgrade

Additional installation for Ubuntu 24.04
-----------------------------------------

::

  sudo apt install libavcodec-dev libavformat-dev libswscale-dev libnsl2 gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly -y

  DEP_PKG_LIST="https://launchpad.net/ubuntu/+archive/primary/+files/libmpdec3_2.5.1-2build2_amd64.deb \
      https://launchpad.net/ubuntu/+archive/primary/+files/libpython3.10-minimal_3.10.4-3_amd64.deb \
      https://launchpad.net/ubuntu/+archive/primary/+files/libpython3.10-stdlib_3.10.4-3_amd64.deb \
      https://launchpad.net/ubuntu/+archive/primary/+files/libpython3.10_3.10.4-3_amd64.deb \
      https://launchpad.net/ubuntu/+archive/primary/+files/libprotobuf23_3.12.4-1ubuntu7_amd64.deb \
      https://launchpad.net/ubuntu/+archive/primary/+files/libgoogle-glog0v5_0.5.0+really0.4.0-2_amd64.deb \
      https://launchpad.net/ubuntu/+archive/primary/+files/libtiff5_4.3.0-6_amd64.deb \
      https://launchpad.net/ubuntu/+archive/primary/+files/libilmbase25_2.5.7-2_amd64.deb \
      https://launchpad.net/ubuntu/+archive/primary/+files/libopenexr25_2.5.7-1_amd64.deb"

  for pkg in $DEP_PKG_LIST
  do
      echo $pkg
      wget $pkg
      sudo dpkg -i *.deb
      rm *.deb
  done

*******************************************
Programming guide for C++ Applications
*******************************************

Incorporating the Ryzen AI's optimized features into C++ applications can be
done in a few simple steps, as explained in the following sections.

Include Ryzen AI CVML library headers
======================================

The required definitions for compiling each Ryzen AI feature are included in a
corresponding header file under the **include/** folder: ::

  cvml-feature-name.h

where ``feature-name`` is the name of the desired Ryzen AI feature.

For example, the definitions for the Ryzen AI Depth Estimation feature are
available after adding a line similar to the following example: ::

  #include <cvml-depth-estimation.h>

Details about each feature's programming interface and expected usage are
provided within their individual include headers.

Create Ryzen AI CVML library context
======================================

Each Ryzen AI CVML library feature is created against a *CVML context* (see ``amd::cvml::Context``).
The context provides access to common functions for logging, etc. A pointer to a new
context may be obtained by calling the ``amd::cvml::CreateContext()`` function: ::

  auto ryzenai_context = amd::cvml::CreateContext();

When no longer needed, the context may be released using its ``Release()``
member function: ::

  ryzenai_context->Release();

Create Ryzen AI CVML library feature object
=============================================

The application programming interface for each feature is provided via a
*Ryzen AI CVML library C++ feature object* that might be instantiated once a
Ryzen AI CVML library context has been created.

The following example instantiates a feature object for the depth estimation
library: ::

  amd::cvml::DepthEstimation ryzenai_depth_estimation(ryzenai_context);

Encapsulate image buffers
==========================

The Ryzen AI CVML library defines its own *Image* class (see ``amd::cvml::Image``) for
representing images and video frame buffers. Each *Image* object is assigned a
specific format and data type on creation. For example, an *Image* to encapsulate
an incoming RGB888 frame buffer can be created with the following code: ::

  amd::cvml::Image ryzenai_image(amd::cvml::Image::Format::kRGB,
                                 amd::cvml::Image::DataType::kUint8, width,
                                 height, data_pointer);

Execute the feature
====================

To execute a Ryzen AI feature on a provided input, call the appropriate
*execution* member function of the Ryzen AI CVML library feature object.

For example, the following code executes a single instance of the depth
estimation library, using the *ryzenai_image* from the previous section: ::

  // encapsulate output buffer
  amd::cvml::Image ryzenai_output(amd::cvml::Image::Format::kGrayScale,
                                  amd::cvml::Image::DataType::kFloat32,
                                  output_width, output_height, output_pointer);

  // execute the feature
  ryzenai_depth_estimation.GenerateDepthMap(ryzenai_image, &ryzenai_output);

*****************************************************
Building applications with Ryzen AI CVML Libraries
*****************************************************

When building applications against the Ryzen AI CVML library, ensure that the
library's ``include/`` folder is part of the compiler's include paths, and that
the library's ``windows/`` or ``linux/`` folder has been added to the linker's
library paths.

Depending on the application's build environment, it might also be necessary to
explicitly list which of the Ryzen AI CVML library's .LIB files (when building for
Windows applications) need to be linked.

Building Ryzen AI CVML library applications with CMake
=======================================================

If CMake is used for the application's build environment, the necessary
include folder and link libraries can be added with the following lines
in the application's ``CMakeLists.txt`` file: ::

  # find Ryzen AI CVML library and set include folders
  find_package(RyzenAILibrary REQUIRED PATHS ${AMD_CVML_SDK_ROOT})

  # add Ryzen AI CVML library linker libraries
  target_link_libraries(${PROJECT_NAME} ${RyzenAILibrary_LIBS})

where ``AMD_CVML_SDK_ROOT`` defines the location of the Ryzen AI CVML library files and
``PROJECT_NAME`` defines the name of the application build target.

Building Ryzen AI CVML library sample applications
===================================================

In addition to general Ryzen AI CVML library prerequisite and dependencies listed
under `Prerequisites and dependencies`_, the included sample
applications also make use of OpenCV for reading input images/videos/camera
and displaying final output windows. A copy of `OpenCV <https://opencv.org/>`_
will need to be downloaded to the development system before the samples can
be rebuilt and/or executed. Note that CVML samples are built and tested with OpenCV 4.11 on both Windows and Linux.

Ensure the following prerequisites have been set up to build Ryzen AI CVML library sample applications:

- CMake has been installed and is available in the system/user path
- On Windows, Visual Studio's "Desktop development with C++" build tools, or a comparable C++ toolchain, has been installed
- The location of OpenCV libraries has been assigned to the ``OPENCV_INSTALL_ROOT`` environment variable
- The relative locations of the ``include``, ``windows``, ``linux``, and ``samples`` folders are unchanged

The following are CMake commands for building samples.

On Windows, ::

  rem Point to the build subfolder inside your OpenCV installation
 rem (for exampleif you extracted OpenCV to C:\opencv, use C:\opencv\build)
  rem CMake's find_package needs this folder to locate OpenCVConfig.cmake
  set OPENCV_INSTALL_ROOT=C:\opencv\build
  cd samples/
  mkdir build
  cmake -S %CD% -B %CD%\build -DOPENCV_INSTALL_ROOT=%OPENCV_INSTALL_ROOT% -DCMAKE_PREFIX_PATH=%OPENCV_INSTALL_ROOT%
  cmake --build %CD%\build --config Release

On Linux, ::

  export OPENCV_INSTALL_ROOT=<Path to OpenCV Libraries>
  cd samples/
  mkdir build
  cmake -S $PWD -B $PWD/build -DOPENCV_INSTALL_ROOT="$OPENCV_INSTALL_ROOT" -DCMAKE_PREFIX_PATH="$OPENCV_INSTALL_ROOT"
  cmake --build $PWD/build --config Release

*************************************************
Running Ryzen AI CVML library sample applications
*************************************************

This section describes how to execute Ryzen AI CVML library sample applications.

Locating Ryzen AI CVML library runtime files
=============================================

When executing applications built against the Ryzen AI CVML library, ensure that the runtime files are accessible as described below for each platform. For both Windows and Linux, add OpenCV runtime libs to PATH.

.. _windows_execution:

For Windows, either one of the following conditions are met:

1. The Ryzen AI CVML library runtime dll and graphlib files are in the same folder as the application executable.
2. The Ryzen AI CVML library's **windows/** folder has been added to the PATH environment variable.

::

  set PATH=<location of Ryzen AI CVML library package>\windows;%PATH%
  set PATH=%OPENCV_INSTALL_ROOT%\x64\vc16\bin;%PATH%

.. _linux_execution:

For Linux, all the following conditions are met:

1. Add location of **linux/** to LD_LIBRARY_PATH
2. Add location of NPU driver libs (``/opt/xilinx/xrt/lib``) to LD_LIBRARY_PATH

::

  export LD_LIBRARY_PATH=<location of Ryzen AI CVML library package>/linux:$LD_LIBRARY_PATH
  export LD_LIBRARY_PATH=/opt/xilinx/xrt/lib:$LD_LIBRARY_PATH
  export LD_LIBRARY_PATH=$OPENCV_INSTALL_ROOT/lib:$LD_LIBRARY_PATH

Select an input source/image/video
====================================

Ryzen AI CVML library samples can accept a variety of image and video input formats, or even open the default camera on the system if "0" is specified as an input.

In this example, a publicly available video file is used for the application's input. ::

  curl -o dancing.mp4 https://videos.pexels.com/video-files/4540332/4540332-hd_1920_1080_25fps.mp4

Execute the sample application
================================

Finally, the previously built sample application can be executed with the selected input source.

On Windows, ::

  build\cvml-sample-depth-estimation\Release\cvml-sample-depth-estimation.exe -i dancing.mp4

On Linux, ::

  ./build/cvml-sample-depth-estimation/cvml-sample-depth-estimation -i dancing.mp4


..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.

