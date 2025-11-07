#########################
Linux Installation Instructions
#########################

Ryzen AI for Linux supports compiling and running AI models on the AMD Neural Processing Unit (NPU). The current release supports the following model types:

- CNN models in INT8 format
- CNN models in BF16 format
- NLP models (e.g., BERT, encoder-based) in BF16 format
- LLMs (NPU-only flow)


*************
Prerequisites
*************

.. list-table::
   :widths: 25 25
   :header-rows: 1

   * - Dependencies
     - Version Requirement
   * - Ubuntu Distribution
     - Ubuntu 24.04 LTS
   * - Kernel Version
     - >= 6.10
   * - RAM
     - 32GB or Higher, 64GB (Recommended)
   * - Python
     - 3.10.x


Use the commands below to install Python 3.10.x along with certain dependencies

.. code-block:: bash

  sudo apt-get install python3.10
  sudo apt-get install python3.10-venv

After installing required Ubuntu distribution and Python version, proceed with NPU drivers installation

.. _install-driver:

*******************
Install NPU Drivers
*******************
- Download the NPU driver package from `Downloads` section of `Ryzen AI Software Early Access Lounge <https://account.amd.com/en/member/ryzenai-sw-ea.html#tabs-a5e122f973-item-4757898120-tab>`_.

- RyzenAI linux driver package contains 
   - XRT Package
      - xrt_202520.2.20.122_24.04-amd64-base.deb
      - xrt_202520.2.20.122_24.04-amd64-base-dev.deb
      - xrt_202520.2.20.122_24.04-amd64-npu.deb

   - NPU driver package
      - xrt_plugin.2.20.250102.48.release_24.04-amd64-amdxdna.deb

- Install NPU driver package on your machine

.. code-block:: bash

   sudo apt reinstall --fix-broken -y ./xrt_202520.2.20.122_24.04-amd64-base.deb
   sudo apt reinstall --fix-broken -y ./xrt_202520.2.20.122_24.04-amd64-base-dev.deb
   sudo apt reinstall --fix-broken -y ./xrt_202520.2.20.122_24.04-amd64-npu.deb
   sudo apt reinstall --fix-broken -y ./xrt_plugin.2.20.250102.48.release_24.04-amd64-amdxdna.deb


- Set essential Environment variables 
.. code-block:: bash

   export LD_LIBRARY_PATH=/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH
   source /opt/xilinx/xrt/setup.sh

- Verify your Driver installation

.. code-block:: bash

   xrt-smi examine

   Device(s) Present
   |BDF             |Name       |
   |----------------|-----------|
   |[0000:c5:00.1]  |NPU Strix  |


.. _install-bundled:

*************************
Install Ryzen AI Software
*************************
- Download the RyzenAI for Linux package `ryzen_ai-1.6.1.tgz` from `Downloads` section of `Ryzen AI Software Early Access Lounge <https://account.amd.com/en/member/ryzenai-sw-ea.html#tabs-a5e122f973-item-4757898120-tab>`_.
- Navigate to the downloaded path and follow the below steps

.. code-block:: bash

   mkdir ryzen_ai-1.6.1
   cp ryzen_ai-1.6.1.tgz ryzen_ai-1.6.1

   cd ryzen_ai-1.6.1
   tar -xvzf ryzen_ai-1.6.1.tgz 
   

- Install RyzenAI package at your desired target path

.. code-block:: bash

   ./install_ryzen_ai.sh -a yes -p <TARGET-PATH>/venv
   source <TARGET-PATH>/venv/bin/activate

- This will successfully install RyzenAI and activate the Virtual environment at your target location

.. code-block:: bash
   
   # Validate your installation path
   echo $RYZEN_AI_INSTALLATION_PATH


**********************
Test the Installation
**********************
The RyzenAI software package contains a test script that verifies your correct installation of NPU Drivers.

- Navigate to your targeted Virtual Environment created in the previous step
- You will observe a subfolder named "quicktest"

.. code-block:: bash

   cd <TARGET-PATH>/venv/quicktest
   python quicktest.py

- The quicktest.py script picks up a simple CNN model, compiles it and runs on AMD's Neural Processing Unit (NPU). 
- On successful run, you can observe output as shown below.

.. code-block:: bash

   Setting environment for STX
   WARNING: Logging before InitGoogleLogging() is written to STDERR
   I20250714 14:46:51.976055 139787 vitisai_compile_model.cpp:1157] Vitis AI EP Load ONNX Model Success
   I20250714 14:46:51.976090 139787 vitisai_compile_model.cpp:1158] Graph Input Node Name/Shape (1)
   I20250714 14:46:51.976099 139787 vitisai_compile_model.cpp:1162] 	 input : [-1x3x32x32]
   I20250714 14:46:51.976104 139787 vitisai_compile_model.cpp:1168] Graph Output Node Name/Shape (1)
   I20250714 14:46:51.976109 139787 vitisai_compile_model.cpp:1172] 	 output : [-1x10]

   [Vitis AI EP] No. of Operators :   NPU   398 VITIS_EP_CPU     2 
   [Vitis AI EP] No. of Subgraphs :   NPU     1 Actually running on NPU     1 
   Test Passed



************************
Examples, Demos, Tutorials
************************

- RyzenAI-SW demonstrates various demos and examples for Model compilation and deployment on NPUs

- Here are a few examples from our `RyzenAI Software Repository <https://github.com/amd/RyzenAI-SW/tree/main>`_
   - `Getting started Resnet with BF16 Model <https://github.com/amd/RyzenAI-SW/tree/main/tutorial/getting_started_resnet/bf16>`_
   - `Getting started Resnet with INT8 Model <https://github.com/amd/RyzenAI-SW/tree/main/tutorial/getting_started_resnet/int8>`_
   - `Yolov8m Model for Object Detection <https://github.com/amd/RyzenAI-SW/tree/main/tutorial/object_detection>`_


.. note::

   Before running the above examples - 
      - RyzenAI creates its own Python Virtual Environment to run the examples. You can skip conda environment instruction as they are Windows specific only
      - Ensure to activate Linux based Python Virtual Environment 

.. code-block:: python

  source <TARGET-PATH>/venv/bin/activate


***********
Running LLM
***********

Follow this page to run LLM models on Linux: :doc:`llm_linux`


************
Limitations
************

- Integer CNN Model is only supported through Legacy backend compiler (X1)
- Of all supported LLM models, several require a 64GB machine for running.






