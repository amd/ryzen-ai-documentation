###############################
Linux Installation Instructions
###############################


Ryzen AI for Linux supports running AI models on the AMD Neural Processing Unit (NPU).
The current release supports STX and KRK platforms.

With this release, users can now compile and run AI models using the following formats:

- CNN models in INT8
- CNN models in BF16
- NLP models (e.g., BERT, encoder-based) in BF16
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
     - 64GB (Recommended)
   * - Python
     - 3.12.x


Use the commands below to install Python 3.12.x along with certain dependencies

.. code-block:: bash

  sudo apt update
  sudo apt install python3.12
  sudo apt install python3.12-venv
  sudo apt install libboost-filesystem1.74.0

After installing required Ubuntu distribution and Python version, proceed with NPU drivers installation

.. _install-driver:

*******************
Install NPU Drivers
*******************
- Download the NPU driver package from `Downloads` section of `Ryzen AI Software Drivers <https://account.amd.com/en/forms/downloads/xef.html?filename=RAI_1.7.1_Linux_NPU_XRT.zip>`_.

- RyzenAI linux driver package contains 
   - XRT Package
      - xrt_202610.2.21.75_24.04-amd64-base.deb
      - xrt_202610.2.21.75_24.04-amd64-base-dev.deb
      - xrt_202610.2.21.75_24.04-amd64-npu.deb

   - NPU driver package
      - xrt_plugin.2.21.260102.53.release_24.04-amd64-amdxdna.deb


- Install NPU driver package on your machine

.. code-block:: bash

   sudo apt install --fix-broken -y ./xrt_202610.2.21.75_24.04-amd64-base.deb
   sudo apt install --fix-broken -y ./xrt_202610.2.21.75_24.04-amd64-base-dev.deb
   sudo apt install --fix-broken -y ./xrt_202610.2.21.75_24.04-amd64-npu.deb
   sudo apt install --fix-broken -y ./xrt_plugin.2.21.260102.53.release_24.04-amd64-amdxdna.deb


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

   # NPU name might differ based on your machine

.. _install-bundled:

*************************
Install Ryzen AI Software
*************************
- Download the RyzenAI for Linux package `ryzen_ai-1.7.1.tgz` from `Downloads` section of `Ryzen AI Software Installer <https://account.amd.com/en/forms/downloads/xef.html?filename=ryzen_ai-1.7.1.tgz>`_.
- Navigate to the downloaded path and follow the below steps

.. code-block:: bash

   mkdir ryzen_ai-1.7.1
   cp ryzen_ai-1.7.1.tgz ryzen_ai-1.7.1

   cd ryzen_ai-1.7.1
   tar -xvzf ryzen_ai-1.7.1.tgz 
   

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

   Setting environment for STX/KRK
   
   Test Finished



**************************
Examples, Demos, Tutorials
**************************

- RyzenAI-SW demonstrates various demos and examples for Model compilation and deployment on NPUs

- Here are a few examples from our `RyzenAI Software Repository <https://github.com/amd/RyzenAI-SW/tree/main>`_
   - `Getting started Resnet with BF16 Model <https://github.com/amd/RyzenAI-SW/tree/main/CNN-examples/getting_started_resnet/bf16>`_
   - `Getting started Resnet with INT8 Model <https://github.com/amd/RyzenAI-SW/tree/main/CNN-examples/getting_started_resnet/int8>`_
   - `Yolov8m Model for Object Detection <https://github.com/amd/RyzenAI-SW/tree/main/CNN-examples/object_detection>`_


******
Note
******

Before running the above examples - 
   - RyzenAI creates its own Python Virtual Environment to run the examples. You can skip conda environment instruction as they are Windows specific only
   - Ensure to activate Linux based Python Virtual Environment 

.. code-block:: bash

   source <TARGET-PATH>/venv/bin/activate

=============================
Get NPU Info for your Machine
=============================

`Getting started Resnet with INT8 Model <https://github.com/amd/RyzenAI-SW/tree/main/CNN-examples/getting_started_resnet/int8>`_

Getting started Resnet with INT8 Model contains Resnet_util.py script that has a function "get_npu_info" to detect correct "NPU type" in your machine. This NPU lookup logic is based for Windows system.

For Linux, NPU lookup logic is shown below:

.. code-block:: python

   import subprocess
   
   def get_npu_info():
       # Run below command as subprocess to enumerate PCI devices
       command = r'lspci -nn'
       process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
       stdout, stderr = process.communicate()
      
       # Check for supported Hardware IDs
       npu_type = ''
       if '1022:17f0' in stdout.decode(): npu_type = 'STX/KRK'
       return npu_type
   
   

***********
Running LLM
***********

Follow this page to run LLM models on Linux: :doc:`llm_linux`








