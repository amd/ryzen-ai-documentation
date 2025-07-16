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
   * - Python
     - 3.10.x

Use the commands below to install Python 3.10.x along with certain dependecies

.. code-block::

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

.. code-block::

   sudo apt reinstall --fix-broken -y ./xrt_202520.2.20.41_24.04-amd64-base.deb
   sudo apt reinstall --fix-broken -y ./xrt_202520.2.20.41_24.04-amd64-base-dev.deb
   sudo apt reinstall --fix-broken -y ./xrt_202520.2.20.41_24.04-amd64-npu.deb 
   sudo apt reinstall --fix-broken -y ./xrt_plugin.2.20.250102.3.rel_24.04-amd64-amdxdna.deb
   export LD_LIBRARY_PATH=/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH
   source /opt/xilinx/xrt/setup.sh

- To verify your Driver installation, you can run the command:

.. code-block::

   /opt/xilinx/xrt/bin/xrt-smi examine

   Device(s) Present
   |BDF             |Name       |
   |----------------|-----------|
   |[0000:c5:00.1]  |NPU Strix  |


.. note:

   Whenever you restart your linux  


.. _install-bundled:

*************************
Install Ryzen AI Software
*************************
- Download the RyzenAI for Linux package :download:`ryzen-ai-1.5.0.tgz <https://xcoartifactory/ui/native/vaiml-installers-prod-local/installers/rai-1.5.0/latest/lnx64/ryzen_ai-1.5.0.tgz>`
- Navigate to the downloaded path and follow the below steps

.. code-block::

   tar -xvzf ryzen_ai-1.5.0.tgz 
   cd ryzen-ai-1.5.0

- Install RyzenAI package at your desired target path

.. code-block::

   ./install_ryzen_ai_1_5.sh -a yes -p <TARGET-PATH/venv>
   source <TARGET-PATH/venv>/bin/activate

- This will successfully install RyzenAI and activate the Virtual environment at your targeted location.



**********************
Test the Installation
**********************
The RyzenAI software package contains a test script that verifies your correct installation of NPU Drivers.

- Navigate to your targeted Virtual Environment created in the previous step
- You will observe a subfolder named "quicktest"

.. code-block::

   cd <TARGET-PATH/venv/quicktest>
   python quicktest.py

- The quicktest.py script picks up a simple CNN model, compiles it and runs on AMD's Neural Processing Unit (NPU). 
- On successful run, you can observe output as shown below.

.. code-block::

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


