#########################
Linux Installation Instructions
#########################

Ryzen AI for linux supports compiling the AI models and running on AMD processor- Neural Processing Unit (NPU). 

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
     - 32GB or Higher
   * - Python
     - 3.10.x

Use the commands below to install Python 3.10.x along with certain dependecies

.. code-block:: bash

  sudo apt-get install python3.10
  sudo apt-get install python3.10-venv

Once you have correct Ubuntu distribution and Python installed locally, you can proceed with NPU drivers installation

.. _install-driver:

*******************
Install NPU Drivers
*******************
- Download the NPU driver package from this link :download:`NPU Driver <https://mkmartifactory.amd.com:8443/artifactory/atg-cvml-generic-local/builds/Linux-ipu/Release/IPU_RC3_25.06.24/jenkins-CVML-Release-linux-ipu-sw-release-40/build/>`

- RyzenAI linux driver package contains 
   - XRT Package
      - xrt_202520.2.20.41_24.04-amd64-base.deb
      - xrt_202520.2.20.41_24.04-amd64-base-dev.deb
      - xrt_202520.2.20.41_24.04-amd64-npu.deb

   - NPU driver package
      - xrt_plugin.2.20.250102.3.rel_24.04-amd64-amdxdna.deb

- Follow the instructions below to install NPU driver package

.. code-block:: bash

   sudo apt reinstall --fix-broken -y ./xrt_202520.2.20.41_24.04-amd64-base.deb
   sudo apt reinstall --fix-broken -y ./xrt_202520.2.20.41_24.04-amd64-base-dev.deb
   sudo apt reinstall --fix-broken -y ./xrt_202520.2.20.41_24.04-amd64-npu.deb 
   sudo apt reinstall --fix-broken -y ./xrt_plugin.2.20.250102.3.rel_24.04-amd64-amdxdna.deb
   export LD_LIBRARY_PATH=/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH
   source /opt/xilinx/xrt/setup.sh

- To verify your Driver installation, you can run the command:

.. code-block:: bash

   /opt/xilinx/xrt/bin/xrt-smi examine

   Device(s) Present
   |BDF             |Name       |
   |----------------|-----------|
   |[0000:c5:00.1]  |NPU Strix  |

.. note::

   NPU drivers timeout after certain period of inactivity. Wake them up by rerunning the commands below-

   - export LD_LIBRARY_PATH=/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH
   - source /opt/xilinx/xrt/setup.sh
   - /opt/xilinx/xrt/bin/xrt-smi examine

.. _install-bundled:

*************************
Install Ryzen AI Software
*************************
- Download the RyzenAI for Linux package :download:`ryzen-ai-1.5.0.tgz <https://account.amd.com/en/forms/downloads/ryzen-ai-software-platform-xef.html?filename=ryzen_ai-1.5.0.tgz>`
- Navigate to the downloaded path and follow the below steps

.. code-block:: bash

   tar -xvzf ryzen_ai-1.5.0.tgz 
   cd ryzen-ai-1.5.0

- Install RyzenAI package at your desired target path

.. code-block:: bash

   ./install_ryzen_ai_1_5.sh -a yes -p <TARGET-PATH>/venv
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
   Header version 0.1
   Device Generation: 4
   Cols, Rows, NumMemRows : (4, 6, 1)
   TransactionSize: 61320
   NumOps: 1560
   Save/Restore preemption code added for col4
   Header version 1.0
   Device Generation: 4
   Cols, Rows, NumMemRows : (4, 6, 1)
   TransactionSize: 2300
   NumOps: 121
   Optimized HEADER version detected 
   Header version 1.0
   Device Generation: 4
   Cols, Rows, NumMemRows : (4, 6, 1)
   TransactionSize: 2492
   NumOps: 137
   Optimized HEADER version detected 
   UID:2bd37a687997d5d6108146ed193af903
   elf_size: 893768
   [Vitis AI EP] No. of Operators :   NPU   398 VITIS_EP_CPU     2 
   [Vitis AI EP] No. of Subgraphs :   NPU     1 Actually running on NPU     1 
   Test Passed



************************
Examples, Demos, Tutorials
************************

- RyzenAI-SW demonstrates various demos and examples for Model compilation and deployment on NPUs

- We recommend our Getting started Resnet tutorial as an entry to our Linux Environment - `Getting started Resnet with BF16 Model <https://github.com/amd/RyzenAI-SW/tree/main/tutorial/linux>`_

*******************
Additional Examples
*******************
- Here are a few more examples from our `RyzenAI Software Repository <https://github.com/amd/RyzenAI-SW/tree/main>`_
   - `Getting started Resnet with INT8 Model <https://github.com/amd/RyzenAI-SW/tree/main/tutorial/getting_started_resnet/int8>`_
   - `Yolov8m Model for Object Detection <https://github.com/amd/RyzenAI-SW/tree/main/tutorial/object_detection>`_

.. note::

   Before running the above examples - 
      - RyzenAI creates its own Python Virtual Environment to run the examples. You can skip conda environment instruction as they are Windows specific only
      - Make sure you provide correct XCLBIN path before running any XINT8 model on NPU. (Refer to quicktest snippet below for a reference)

.. code-block:: python


    install_dir = <RyzenAI installation directory>
    xclbin_file = os.path.join(install_dir, 'voe-4.0-linux_x86_64', 'xclbins', 'strix', 'AMD_AIE2P_4x4_Overlay.xclbin')
   
    provider_options = [{
            'cache_dir': cache_dir,
            'cache_key': cache_key,
            'xclbin': xclbin_file
        }]

    # creating a session
    session = ort.InferenceSession(model, providers=providers,
                               provider_options=provider_options)




***************************
C++ Application Development
***************************

- Follow the instructions below to install prerequisites before building Models in C++

- Install GCC 12 and set it as the default compiler

.. code-block:: bash

   sudo apt update
   sudo apt install gcc-12 g++-12
   sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-12 100 --slave /usr/bin/g++ g++ /usr/bin/g++-12
   sudo update-alternatives --config gcc


- Install RyzenAI and Source activate the Environment
- Install cmake with GLIBCXX_3.4.30
.. code-block:: python

   pip install cmake==3.31.6



***********
Running LLM
***********

Please follow this page for :doc:`llm_linux`



