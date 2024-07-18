###################
Manual Installation
###################

The main :doc:`inst` page shows a one-step installation process that checks the prerequisite and installs Vitis AI ONNX quantizer, ONNX Runtime, and Vitis AI execution provider.

This page explains how to install each component manually. 

.. note::

   Make sure to follow the installation steps in the order explained below.

******************************
Perform a Default Installation
******************************

Download the :download:`ryzenai-1.2.0.msi <https://xcoartifactory:443/artifactory/aie-ipu-prod-local/com/xilinx/ryzenai-installer/main/118/ryzenai-1.2.0.msi>` installer.

Install the RyzenAI Software using the default settings. 

This will copy in the ``C:Program Files\RyzenAI\1.2.0`` folder all the files required for a manual installation.


**************************
Create a Conda Environment
**************************

The Ryzen AI Software requires using a conda environment (Anaconda or Miniconda) for the installation process. 

Start a conda prompt. In the conda prompt, create and activate an environment for the rest of the installation process. 

.. code-block:: 

  conda create --name <name> python=3.10
  conda activate <name> 


*************************
Set Environment Variables
*************************

Configure the environment variables to be automatically set upon activation of the conda environment.

First, create a directory for the activation scripts:

.. code-block:: shell

   mkdir %CONDA_PREFIX%\etc\conda\activate.d

Create script to load ``RYZEN_AI_INSTALLER_PATH`` environment. This script will be executed every time the conda environment is activated.

.. code-block:: shell

   notepad %CONDA_PREFIX\etc\conda\activate.d\load_ryzenai_installer_path.bat


Add the following line to the script:

.. code-block:: shell

   set "RYZEN_AI_INSTALLER_PATH=%RYZEN_AI_INSTALLER_PATH%"


Set the XLNX_VART_FIRMWARE environment variable based on your CPU model:

For STX CPU models:

.. code-block::

   set XLNX_VART_FIRMWARE=%RYZEN_AI_INSTALLATION_PATH%/voe-4.0-win_amd64/xclbins/strix/AMD_AIE2P_Nx4_Overlay.xclbin

For PHX/HPT CPU models:

.. code-block::

   set XLNX_VART_FIRMWARE=%RYZEN_AI_INSTALLATION_PATH%/voe-4.0-win_amd64/xclbins/phoenix/1x4.xclbin

.. _install-onnx-quantizer:

******************************
Install the Vitis AI Quantizer
******************************

The :doc:`Vitis AI Quantizer for ONNX <vai_quant/vai_q_onnx>` supports a post-training quantization method that works on models saved in the ONNX format. 

Install the Vitis AI Quantizer for ONNX as follows:

.. code-block:: shell

   cd %RYZEN_AI_INSTALLATION_PATH%
   pip install vai_q_onnx-1.16.0+69bc4f2-py2.py3-none-any.whl

To install other quantization tools (Vitis AI PyTorch/TensorFlow 2/TensorFlow Quantization or Olive Quantization), refer to the :doc:`alternate_quantization_setup` page. 


************************
Install the ONNX Runtime
************************

.. code-block::
   
   pip install onnxruntime 


***************************************
Install the Vitis AI Execution Provider
***************************************

.. code-block:: 

   cd %RYZEN_AI_INSTALLATION_PATH%/voe-4.0-win_amd64
   pip install voe-0.1.0-cp39-cp39-win_amd64.whl
   pip install onnxruntime_vitisai-1.15.1-cp39-cp39-win_amd64.whl
   python installer.py


*********************
Test the Installation
*********************

The Ryzen AI Software installation folder contains a test to verify that the Ryzen AI software is correctly installed. Instructions on how to run this test can be found :ref:`here <quicktest>`.


..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.