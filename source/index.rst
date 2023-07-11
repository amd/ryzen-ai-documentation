########################
Ryzen AI Developer Guide  
########################

The Ryzen AI SDK enables developers to take machine learning models trained in PyTorch or TensorFlow and run them on laptops powered by `AMD Ryzen™ AI <https://www.amd.com/en/products/ryzen-ai>`__. AMD Ryzen AI is a dedicated AI accelerator integrated on-chip with the CPU cores. The Ryzen AI software intelligently optimizes tasks and workloads, freeing-up CPU and GPU resources and ensuring optimal performance at lower power.

|

.. image:: images/rayzenai.png
   :scale: 75%
   :align: center

|
|

*****************
Table of Contents
*****************

Getting Started
===============

* **Installation**: Refer to :doc:`inst` page. 

* **Release Notes**: Refer to :doc:`relnotes` page.

* **Development Flow Overview**: Refer to :doc:`devflow` page. 

* **Getting Started Example**: Refer to :doc:`getstartex` page to run a resnet50 model example

Using Your Model
================

* **Model Compatibility**: Refer to :doc:`modelcompat` page. 

* **Model Quantization**: Refer to :doc:`modelport` page. 

* **Model Running Using ONNX Runtime**: Refer to the :doc:`modelrun` page. 



.. toctree::
   :maxdepth: 1
   :caption: Getting Started
   :hidden:

   inst.rst
   relnotes.rst
   devflow.rst
   getstartex.rst

.. toctree::
   :maxdepth: 1
   :caption: Using Your Model
   :hidden:

   modelcompat.rst
   modelport.rst
   modelrun.rst

..
  ------------
  #####################################
  Please Read: Important Legal Notices
  #####################################
  
  The information presented in this document is for informational purposes only and may contain technical inaccuracies, omissions, and typographical errors. The information contained herein is subject to change and may be rendered inaccurate for many reasons, including but not limited to product and roadmap changes, component and motherboard version changes, new model and/or product releases, product differences between differing manufacturers, software changes, BIOS flashes, firmware upgrades, or the like. Any computer system has risks of security vulnerabilities that cannot be completely prevented or mitigated. AMD assumes no obligation to update or
  otherwise correct or revise this information. However, AMD reserves the right to revise this information and to make changes from time to time to the content hereof without obligation of AMD to notify any person of such revisions or changes. THIS INFORMATION IS PROVIDED "AS IS." AMD MAKES NO REPRESENTATIONS OR WARRANTIES WITH RESPECT TO THE CONTENTS HEREOF AND ASSUMES NO RESPONSIBILITY FOR ANY INACCURACIES, ERRORS, OR OMISSIONS THAT MAY APPEAR IN THIS INFORMATION. AMD SPECIFICALLY
  DISCLAIMS ANY IMPLIED WARRANTIES OF NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR ANY PARTICULAR PURPOSE. IN NO EVENT WILL AMD BE LIABLE TO ANY
  PERSON FOR ANY RELIANCE, DIRECT, INDIRECT, SPECIAL, OR OTHER CONSEQUENTIAL DAMAGES ARISING FROM THE USE OF ANY INFORMATION CONTAINED HEREIN, EVEN IF
  AMD IS EXPRESSLY ADVISED OF THE POSSIBILITY OF SUCH DAMAGES. 

  ##################################
  AUTOMOTIVE APPLICATIONS DISCLAIMER
  ##################################


  AUTOMOTIVE PRODUCTS (IDENTIFIED AS "XA" IN THE PART NUMBER) ARE NOT WARRANTED FOR USE IN THE DEPLOYMENT OF AIRBAGS OR FOR USE IN APPLICATIONS
  THAT AFFECT CONTROL OF A VEHICLE ("SAFETY APPLICATION") UNLESS THERE IS A SAFETY CONCEPT OR REDUNDANCY FEATURE CONSISTENT WITH THE ISO 26262 AUTOMOTIVE SAFETY STANDARD ("SAFETY DESIGN"). CUSTOMER SHALL, PRIOR TO USING OR DISTRIBUTING ANY SYSTEMS THAT INCORPORATE PRODUCTS, THOROUGHLY TEST SUCH SYSTEMS FOR SAFETY PURPOSES. USE OF PRODUCTS IN A SAFETY APPLICATION WITHOUT A SAFETY DESIGN IS FULLY AT THE RISK OF CUSTOMER, SUBJECT ONLY TO APPLICABLE LAWS AND REGULATIONS GOVERNING LIMITATIONS ON PRODUCT LIABILITY.

  #########
  Copyright
  #########


  © Copyright 2023 Advanced Micro Devices, Inc. AMD, the AMD Arrow logo, Ryzen, Vitis AI, and combinations thereof are trademarks of Advanced Micro Devices,
  Inc. AMBA, AMBA Designer, Arm, ARM1176JZ-S, CoreSight, Cortex, PrimeCell, Mali, and MPCore are trademarks of Arm Limited in the US and/or elsewhere. PCI, PCIe, and PCI Express are trademarks of PCI-SIG and used under license. OpenCL and the OpenCL logo are trademarks of Apple Inc. used by permission by Khronos. Other product names used in this publication are for identification purposes only and may be trademarks of their respective companies.

