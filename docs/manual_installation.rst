###################
Manual Installation
###################

The main :doc:`inst` page shows a one-step installation process that checks the prerequisite and installs Vitis AI ONNX quantizer, ONNX Runtime, and Vitis AI execution provider.

This page explains how to install each component manually. 

.. note::

   Make sure to follow the installation steps in the order explained below.

********************
Download the Package
********************

Download the :download:`ryzenai-1.2.0.msi <https://xcoartifactory:443/artifactory/aie-ipu-prod-local/com/xilinx/ryzenai-installer/main/118/ryzenai-1.2.0.msi>`.
Ryzen AI Software installation package and double-click to run it.

This should copy all the necessary files to default location: ``C:Program Files\RyzenAI\1.2.0``

Check the Ryzen AI Software installation using the environmental variable ``RYZEN_AI_INSTALLATION_PATH``

.. code-block::

   echo %RYZEN_AI_INSTALLATION_PATH%

**************************
Create a Conda Environment
**************************

The Ryzen AI Software requires using a conda environment (Anaconda or Miniconda) for the installation process. 

Start a conda prompt. In the conda prompt, create and activate an environment for the rest of the installation process. 

.. code-block:: 

  conda create --name <name> python=3.9
  conda activate <name> 


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


*************
Runtime Setup
*************

Set the following environment variable in the conda environment created above:

.. code-block::
   # For PHX
   set XLNX_VART_FIRMWARE=%RYZEN_AI_INSTALLATION_PATH%\voe-4.0-win_amd64\xclbins\phoenix\1x4.xclbin
   # For STX
   set XLNX_VART_FIRMWARE=%RYZEN_AI_INSTALLATION_PATH%\voe-4.0-win_amd64\xclbins\strix\AMD_AIE2P_Nx4_Overlay.xclbin
   set NUM_OF_DPU_RUNNERS=1

The ``*.xclbin`` files are located in the ``voe-4.0-win_amd64\xclbins`` folder of the Ryzen AI Software installation package. For detailed information and other available options refer to the :doc:`runtime_setup` page.


*********************
Test the Installation
*********************

The RyzenAI software installation folder contains a test to verify that the Ryzen AI software is correctly installed. This installation test can be found in the ``quicktest`` folder.

- Run the test: 

.. code-block::

   cd %RYZEN_AI_INSTALLATION_PATH%\quicktest
   python quicktest.py


- The test runs a simple CNN model. On a successful run, you will see an output similar to the one shown below. This indicates that the model is running on NPU and the installation of the Ryzen AI Software was successful:

.. code-block::
  
   [Vitis AI EP] No. of Operators :   CPU     2    IPU   398  99.50%
   [Vitis AI EP] No. of Subgraphs :   CPU     1    IPU     1 Actually running on IPU     1
   ...
   Test Passed
   ...

..
  ------------
