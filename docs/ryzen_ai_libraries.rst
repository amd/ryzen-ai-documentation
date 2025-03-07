.. Copyright (C) 2023-2025 Advanced Micro Devices, Inc. All rights reserved.

##################################
Ryzen AI Library Quick Start Guide
##################################

The Ryzen AI Libraries are built on top of the Ryzen AI drivers and execution infrastructure to provide powerful AI capabilities to C++ applications without the need for training specific AI models and integrating them into the Ryzen AI framework.

Each Ryzen AI library feature offers a simple C++ application programming interface (API) that can be easily incorporated into existing applications.

******************
Supported Features
******************
This release of the Ryzen AI Library supports the following features:

- Depth Estimation

****************
Package Contents
****************

The following files are included with the Ryzen AI Library package:

cmake/
  Packaging info for CMake's find_package function
include/
  C++ header files
windows/
  Binary files for Windows, including both compile time .LIB files and runtime .DLL files
samples/
  Individual sample applications
LICENSE.txt
  License file

***********************************************
Executing Ryzen AI Library enabled applications
***********************************************
Prerequisites and dependencies
==============================
The AMD Adrenalin and Ryzen AI drivers should be installed before attempting to execute Ryzen AI Library applications.

AMD Adrenalin driver
====================
Install the latest version of the AMD Adrenalin driver from https://www.amd.com/en/support/download/drivers.html.

AMD Ryzen AI driver
===================
Install the latest Ryzen AI NPU driver from https://ryzenai.docs.amd.com/en/latest/inst.html.

***************************************
Locating Ryzen AI Library runtime files
***************************************
When executing Windows applications built against the Ryzen AI Library, ensure that one of the following conditions is met,

  1. The Ryzen AI Library runtime dll's are in the same folder as the application executable.
  2. The Ryzen AI Library's windows/ folder has been added to the PATH environment variable.

**************************************
Programming guide for C++ Applications
**************************************
Incorporating the Ryzen AI's optimized features into C++ applications can be
done in a few simple steps, as explained in the following sections.

Include Ryzen AI Library headers
================================
The required definitions for compiling each Ryzen AI feature are included in a
corresponding,

  cvml-*<feature-name>*.h

header file under the **include/** folder, where *<feature-name>* is the name
of the desired Ryzen AI feature.

For example, the definitions for the Ryzen AI Depth Estimation feature are
available after adding a line similar to the following example::

  #include <cvml-depth-estimation.h>

Details about each feature's programming interface and expected usage are
provided within their individual include headers.

Create Ryzen AI Library context
===============================
Each Ryzen AI Library feature is created against a *CVML context*. The context provides access to common functions for logging and other purposes. A pointer to a new
context may be obtained by calling the *CreateContext()* function::

  auto ryzenai_context = amd::cvml::CreateContext();

When no longer needed, the context may be released using its *Release()*
member function::

  ryzenai_context->Release();

Create Ryzen AI Library feature object
======================================
The application programming interface for each feature is provided through a
*Ryzen AI Library C++ feature object* that may be instantiated afer a
Ryzen AI Library context has been created.

The following example instantiates a feature object for the depth estimation
library::

  amd::cvml::DepthEstimation ryzenai_depth_estimation(ryzenai_context);

Encapsulate image buffers
=========================
The Ryzen AI Library defines its own *Image* class to represent images
and video frame buffers. Each *Image* object is assigned a specific format
and data type on creation. For example, you can use the following code to create an *Image* to encapsulate an incoming
RGB888 frame buffer::

  amd::cvml::Image ryzenai_image(amd::cvml::Image::Format::kRGB,
                                 amd::cvml::Image::DataType::kUint8, width,
                                 height, data_pointer);

Execute the feature
===================
To execute a Ryzen AI feature on a provided input, call the appropriate
*execution* member function of the Ryzen AI Library feature object.

For example, the following code executes a single instance of the depth
estimation library, using the *ryzenai_image* from the previous section::

  // encapsulate output buffer
  amd::cvml::Image ryzenai_output(amd::cvml::Image::Format::kGrayScale,
                                  amd::cvml::Image::DataType::kFloat32,
                                  output_width, output_height, output_pointer);

  // execute the feature
  ryzenai_depth_estimation.GenerateDepthMap(ryzenai_image, &ryzenai_output);

*********************************************
Building applications with Ryzen AI Libraries
*********************************************
When building applications against the Ryzen AI Library, ensure that the
library's,

  include/

folder is part of the compiler's include paths, and that the library's,

  windows/

folder has been added to the linker's library paths.

Depending on the application's build environment, you might also need to
explicitly list which of the Ryzen AI Library's .LIB files (when building for
Windows applications) need to be linked.

*************************************************
Building Ryzen AI Library applications with CMake
*************************************************
If CMake is used for the application's build environment, the necessary include folder and link libraries can be added with the following lines in the application's CMakeLists.txt file::

  // find Ryzen AI Library and set include folders
  find_package(RyzenAILibrary REQUIRED PATHS ${AMD_CVML_SDK_ROOT})

  // add Ryzen AI Library linker libraries
  target_link_libraries(${PROJECT_NAME} ${RyzenAILibrary_LIBS})

where ``AMD_CVML_SDK_ROOT`` defines the location of the Ryzen AI Library files and ``PROJECT_NAME`` defines the name of the application build target.

*********************************************
Building Ryzen AI Library sample applications
*********************************************
In addition to general Ryzen AI Library prerequisite and dependencies listed under Prerequisites and dependencies, the included sample applications also make use of OpenCV for reading input images/videos/camera and displaying final output windows. A copy of OpenCV will need to be downloaded to the development system before the samples can be rebuilt and/or executed.
On Windows platforms, an 'ms-build-samples.bat' file is provided to build all the provided sample applications using CMake:
  
  C:\\ryzen-ai-library-location\\samples> ms-build-samples.bat

The batch file assumes that the following prerequisites have been set up:

  - CMake has been installed and is available in the system/user path
  - Visual Studio's "Desktop development with C++" build tools, or a comparable C++ toolchain, has been installed
  - The location of OpenCV libraries has been assigned to the ``OPENCV_INSTALL_ROOT`` environment variable
  - The relative locations of the ``include``, ``windows`` and ``samples`` folders are unchanged

*******
License
*******
Refer to the LICENSE.txt file for the full license text and copyright notice.

*************************
Copyrights and Trademarks
*************************
**2021 Advanced Micro Devices, Inc.** All rights reserved.

The information contained herein is for informational purposes only, and is subject to change without notice. While every precaution has been taken in the preparation of this document, it may contain technical inaccuracies, omissions and typographical errors, and AMD is under no obligation to update or otherwise correct this information. Advanced Micro Devices, Inc. makes no representations or warranties with respect to the accuracy or completeness of the contents of this document, and assumes no liability of any kind, including the implied warranties of noninfringement, merchantability or fitness for particular purposes, with respect to the operation or use of AMD hardware, software or other products described herein. No license, including implied or arising by estoppel, to any intellectual property rights is granted by this document. Terms and limitations applicable to the purchase or use of AMD's products are as set forth in a signed agreement between the parties or in AMD's Standard Terms and Conditions of Sale. Any unauthorized copying, alteration, distribution, transmission, performance, display or other use of this material is prohibited.

**********
Trademarks
**********

AMD, the AMD Arrow logo, AMD AllDay, AMD Virtualization, AMD-V, PowerPlay, Vari-Bright, and combinations thereof are trademarks of Advanced Micro Devices, Inc. Other product names used in this publication are for identification purposes only and may be trademarks of their respective companies.

Dolby is a trademark of Dolby Laboratories.

HDMI is a trademark of HDMI Licensing, LLC.

HyperTransport is a licensed trademark of the HyperTransport Technology Consortium.

Microsoft, Windows, Windows Vista, and DirectX are registered trademarks of Microsoft Corporation in the US and/or other countries.

PCIe is a registered trademark of PCI-Special Interest Group (PCI-SIG).

USB Type-C ® and USB-C ® are registered trademarks of USB Implementers Forum.

**Dolby Laboratories, Inc.**

Manufactured under license from Dolby Laboratories.

**Rovi Corporation**

This device is protected by U.S. patents and other intellectual property rights. The use of Rovi Corporation's copy protection technology in the device must be authorized by Rovi Corporation and is intended for home and other limited pay-per-view uses only, unless otherwise authorized in writing by Rovi Corporation.

Reverse engineering or disassembly is prohibited.

USE OF THIS PRODUCT IN ANY MANNER THAT COMPLIES WITH THE MPEG ACTUAL OR DE FACTO VIDEO AND/OR AUDIO STANDARDS IS EXPRESSLY PROHIBITED WITHOUT ALL NECESSARY LICENSES UNDER APPLICABLE PATENTS. SUCH LICENSES MAY BE ACQUIRED FROM VARIOUS THIRD PARTIES INCLUDING, BUT NOT LIMITED TO, IN THE MPEG PATENT PORTFOLIO, WHICH LICENSE IS AVAILABLE FROM MPEG LA, L.L.C., 6312 S. FIDDLERS GREEN CIRCLE, SUITE 400E, GREENWOOD VILLAGE, COLORADO 80111.

**xtensor, xtl, xsimd**

Copyright (c) 2016, Johan Mabille, Sylvain Corlay and Wolf Vollprecht Copyright (c) 2016, QuantStack All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

****************
Revision History
****************
+-------------------+----------+--------------------------------+
| Date              | Revision | Notes                          |
+===================+==========+================================+
| December 04, 2023 | 1.0      | Initial revision               |
+-------------------+----------+--------------------------------+
| March 04, 2025    | 1.1      | Include driver/copyright info  |
+-------------------+----------+--------------------------------+

..
  ------------

  #####################################
  License
  #####################################

  Ryzen AI is licensed under MIT License. Refer to the LICENSE file for the full license text and copyright notice.
