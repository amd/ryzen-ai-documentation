#############
Runtime Setup
#############

.. contents:: Table of Contents


IPU Binary selection
~~~~~~~~~~~~~~~~~~~~

The IPU binaries are located inside the Vitis AI Execution Provider package. Selecting an IPU binary is a required step everytime the application is run from a new terminal. Ryzen AI Software platform provides a couple of IPU binaries using different configurations on the IPU device. 

**IPU binary 1x4.xclbin**: An AI stream using 1x4.xclbin uses an IPU configuration that provides up to 2 TOPS performance. Most real-time application (video conferencing use cases) performance requirements can be met using this configuration. In the current Ryzen AI software platform, up to four such AI streams can be run in parallel on the IPU without any visible loss of performance.


**IPU binary 5x4.xclbin**: For more advanced usecases or larger models, IPU binary 5x4.xclbin can be used which uses a larger configuration to provide up to 10 TOPs performance. In the current version of the release, 5x4.xclbin does not support multiple concurrent AI streams, and can only be used by a single application. 


The procedure for selecting a specific binary using environment variables is as follows:

Selecting the 1x4.xclbin IPU binary:

.. code-block::

   set XLNX_VART_FIRMWARE=C:\path\to\1x4.xclbin


Selecting the 5x4.xclbin IPU binary:

.. code-block::

   set XLNX_VART_FIRMWARE=C:\path\to\5x4.xclbin
   set XLNX_TARGET_NAME="AMD_AIE2_5x4_Overlay"

Note: To select the 5x4.xclbin as the IPU binary, the additional XLNX_TARGET_NAME environment variable is required. 


Runtime Configuration File
~~~~~~~~~~~~~~~~~~~~~~~~~~

The Execution Provider setup package contains the Vitis AI Execution Provider runtime configuration file ``vaip_config.json``. This file is required when configuring Vitis AI Execution Provider (VAI EP) inside the ONNX Runtime code.
