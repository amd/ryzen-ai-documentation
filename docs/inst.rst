#########################
Installation Instructions
#########################

************************
Supported Configurations
************************

The Ryzen AI Software supports the following processors running Windows 11

- AMD Ryzen™ 7940HS, 7840HS, 7640HS, 7840U, 7640U.
- AMD Ryzen™ 8640U, 8640HS, 8645H, 8840U, 8840HS, 8845H, 8945H. 

.. note::
   In this documentation, "NPU" is used in descriptions, while "IPU" is retained in the tool's language, code, screenshots, and commands. This intentional 
   distinction aligns with existing tool references and does not affect functionality. Avoid making replacements in the code.

******************
Prepare the System
******************


.. note::

   For the Phonics device with the latest Windows OS build (22631.3527 and above), . \npu_sw_installer.exe installs the new MCDM driver from this 1.2 release.

   If you already have the WDF driver from a previous release, uninstall it by following these steps:

   - Open "Device Manager."
   - Navigate to "System Devices."
   - Find and right-click on "AMD IPU Device."
   - Select "Uninstall device."
   - Check the box for "Attempt to remove the driver for this device."
Click "Uninstall."

Download the NPU Installer :download:`NPU Driver <http://xcoartifactory/ui/native/aie-ipu-prod-local/com/xilinx/ryzenai-installer/npu-driver/rai-1.2-ea1/ipu-driver-1_2.zip>` and install it by following these steps:


1. Extract the downloaded ``ipu-driver-1_2.zip`` zip file.
2. Extract the ``RYZEN AI RELEASE 1.2 <Tag>.zip`` zip file.
3. Open a terminal in administrator mode and execute the ``.\npu_sw_installer.exe`` exe file.

Ensure that the NPU driver is installed from ``Device Manager`` -> ``Neural processors`` -> ``NPU Compute Accelerator Device`` as shown in the following image.

.. image:: images/npu_driver_1.2.png
   :align: center
   :width: 400 px

|
|

To enable the development and deployment of applications leveraging the NPU, you must have the following software installed on the system.


.. list-table:: 
   :widths: 25 25 
   :header-rows: 1

   * - Dependencies
     - Version Requirement
   * - Visual Studio
     - 2022
   * - cmake
     - version >= 3.26
   * - python
     - version >= 3.10 
   * - opencv
     - version == 4.6.0
   * - Anaconda or Miniconda
     - Latest version
|
|
**Note:** Visual Studio 2022 Community edition, ensure "Desktop Development with C++" is installed


.. _install-bundled:

*****************************
Install the Ryzen AI Software
*****************************

Before installing the Ryzen AI Software, ensure that all the prerequisites outlined previously have been met and that the Windows PATH variable is properly set for each component. 
For example, Anaconda requires following paths to be set in the PATH variable ``path\to\anaconda3\``, ``path\to\anaconda3\Scripts\``, ``path\to\anaconda3\Lib\bin\``. 
The PATH variable should be set through the *Environment Variables* window of the *System Properties*. 

Download the RyzenAI Software (MSI) installer :download:`ryzenai-1.2.0.msi <https://xcoartifactory:443/artifactory/aie-ipu-prod-local/com/xilinx/ryzenai-installer/main/118/ryzenai-1.2.0.msi>`

Double click of the MSI installer to start the installation steps. Follows the instructions on the GUI.

During the installation process:

- Accept the terms of the Licence agreement
- Provide the destination folder for RyzenAI installation or use the default location: ``C:Program Files\RyzenAI\1.2.0``
- Specify the name for the conda environment, default name: ``ryzen-ai-1.2.0``

Installation process does the following:

- Copies the necessary files to ``C:Program Files\RyzenAI\1.2.0`` (Default location)
- Creates a conda environment
- Installs all the dependencies within the conda env
- Installs the :doc:`vai_quant/vai_q_onnx`
- Installs the `ONNX Runtime <https://onnxruntime.ai/>`_
- Installs the :doc:`Vitis AI Execution Provider <modelrun>`
- Configures the environment to use the throughput profile of the NPU
- Prints the name of the conda environment before exiting 

The default Ryzen AI Software packages are now installed in the conda environment created by the installer. You can start using the Ryzen AI Software by activating the conda environment created by the installer (the name of the environment is printed during the installation process). 

Check the Ryzen AI Software installation folder using the environmental variable ``RYZEN_AI_INSTALLATION_PATH``

.. code-block::

   echo %RYZEN_AI_INSTALLATION_PATH%
|
|

**IMPORTANT:** The Ryzen AI Software installation folder (``RYZEN_AI_INSTALLATION_PATH``) contains various files required at runtime by the inference session. 
These files include the NPU binaries (:file:`*.xclbin`) and the default runtime configuration file (:file:`vaip_config.json`) for the Vitis AI Execution Provider. 
Refer to the :doc:`runtime_setup` page for more details about setting up the environment before running an inference session on the NPU.

- Instead of the automated installation process, you can install each component manually by following the instructions on the :doc:`manual_installation` page.

- To use your existing conda environment with the Ryzen AI software, follow the :doc:`manual_installation` instructions and manually install the Vitis AI ONNX Quantizer, the ONNX Runtime, and the Vitis AI Execution Provider, without creating a new conda environment.

- If you need to install the Vitis AI PyTorch/TensorFlow Quantizer or the Microsoft Olive Quantizer, refer to the :doc:`alternate_quantization_setup` page. 

*********************
Test the Installation
*********************

The Ryzen AI Software installation folder contains test to verify that the software is correctly installed. This installation test can be found in the ``quicktest`` folder.

Open Anaconda command prompt with administrator access. Adiministrator access is needed to create temporary directories when running the tests.

- Activate the conda environment:

.. code-block::

   conda activate <env_name>

**Note:** Make sure the environment variable XLNX_VART_FIRMWARE is set to the correct *.xclbin from the VOE package.

For STX (default):

.. code-block::

   set XLNX_VART_FIRMWARE=%RYZEN_AI_INSTALLATION_PATH%/voe-4.0-win_amd64/xclbins/strix/AMD_AIE2P_Nx4_Overlay.xclbin

For PHX:

.. code-block::

   set XLNX_VART_FIRMWARE=%RYZEN_AI_INSTALLATION_PATH%/voe-4.0-win_amd64/xclbins/phoenix/1x4.xclbin

- Run the test: 

.. code-block::

   cd %RYZEN_AI_INSTALLATION_PATH%/quicktest
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

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
