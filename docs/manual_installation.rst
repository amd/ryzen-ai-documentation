###################
Manual Installation
###################

The primary :doc:`inst` explain how to automatically install all components of the Ryzen AI Software in a new Conda environment. This page explains how to manually each component in a custom Conda environment.

.. note::

   Make sure to follow the installation steps in the order explained below.

******************************
Perform a Default Installation
******************************

Install the latest NPU driver and Ryzen AI Software by following the steps in the primary :doc:`inst`. 

- When installing the Ryzen AI Software, use the default settings.
- This will copy in the ``C:\Program Files\RyzenAI\1.3.1`` folder all the files required for a manual installation.


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


Set the XLNX_VART_FIRMWARE environment variable based on your APU type:

For STX/KRK APUs:

.. code-block::

   set XLNX_VART_FIRMWARE=%RYZEN_AI_INSTALLATION_PATH%/voe-4.0-win_amd64/xclbins/strix/AMD_AIE2P_Nx4_Overlay.xclbin

For PHX/HPT APUls:

.. code-block::

   set XLNX_VART_FIRMWARE=%RYZEN_AI_INSTALLATION_PATH%/voe-4.0-win_amd64/xclbins/phoenix/1x4.xclbin

.. _install-onnx-quantizer:

***********************
Install Quark Quantizer
***********************

Install Quark quantizer wheel  

.. code-block::

        cd %RYZEN_AI_INSTALLATION_PATH%
        pip install quark-0.6.0-py3-none-any.whl


***************************************
Install the Vitis AI Execution Provider
***************************************

.. code-block:: 

     cd %RYZEN_AI_INSTALLATION_PATH%
     pip install voe-1.3.0-cp310-cp310-win_amd64.whl
     pip install onnxruntime_vitisai-1.19.0-cp310-cp310-win_amd64.whl
     pip install numpy==1.26.4
     

*********************************
Optional: Install the AI Analyzer
*********************************

.. code-block::

     cd %RYZEN_AI_INSTALLATION_PATH%
     pip install aianalyzer-1.3.0-py3-none-any.whl

*************
Runtime Setup
*************

Set the following environment variable in the conda environment created above:

For STX/KRK: (default)

.. code-block::

   set XLNX_VART_FIRMWARE=%RYZEN_AI_INSTALLATION_PATH%\voe-4.0-win_amd64\xclbins\strix\AMD_AIE2P_Nx4_Overlay.xclbin


For PHX/HPT:

.. code-block::

   set XLNX_VART_FIRMWARE=%RYZEN_AI_INSTALLATION_PATH%\voe-4.0-win_amd64\xclbins\phoenix\1x4.xclbin


The ``*.xclbin`` files are located in the ``voe-4.0-win_amd64\xclbins`` folder of the Ryzen AI Software installation package. For detailed information and other available options refer to the :doc:`runtime_setup` page.

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
