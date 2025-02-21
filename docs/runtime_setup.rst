
.. include:: icons.txt

#############
Runtime Setup
#############

.. _driver-compatibility:


*************************************
VitisAI EP / NPU Driver Compatibility
*************************************

The VitisAI EP requires a compatible version of the NPU drivers. For each version of the VitisAI EP, compatible drivers are bounded by a minimum version and a maximum release date. NPU drivers are backward compatible with VitisAI EP released up to 3 years before. The maximum driver release date is therefore set to 3 years after the release date of the corresponding VitisAI EP.

The table below summarizes the driver requirements for the different versions of the VitisAI EP.

.. list-table:: 
   :header-rows: 1

   * - VitisAI EP version
     - Minimum NPU Driver version
     - Maximum NPU Driver release date 
   * - 1.3.1
     - 32.0.203.242
     - January 17th, 2028
   * - 1.3
     - 32.0.203.237
     - November 26th, 2027
   * - 1.2
     - 32.0.201.204
     - July 30th, 2027

.. _apu-types:

*****************
APU Types
*****************

The Ryzen AI Software supports different types of NPU-enabled APUs. These APU types are referred to as PHX, HPT, STX and KRK. 

To programmatically determine the type of the local APU, it is possible to enumerate the PCI devices and check for an instance with a matching Hardware ID.

.. list-table:: 
   :header-rows: 1

   * - Vendor
     - Device
     - Revision
     - APU Type
   * - 0x1022
     - 0x1502
     - 0x00
     - PHX or HPT 
   * - 0x1022
     - 0x17F0
     - 0x00
     - STX 
   * - 0x1022
     - 0x17F0
     - 0x10
     - STX 
   * - 0x1022
     - 0x17F0
     - 0x11
     - STX 
   * - 0x1022
     - 0x17F0
     - 0x20
     - KRK

.. _npu-configurations:

*******************************
NPU Configurations 
*******************************

The Ryzen AI Software currently supports two NPU configurations: the standard configuration and the benchmark configuration.

|warning| **IMPORTANT**: Selecting a NPU configuration is a mandatory step before running an application from a new environment. A configurations is selected by loading the corresponding NPU binary file (.xclbin). 


Standard Configuration
======================

The standard configuration is designed to minimize NPU hardware resource usage, featuring a smaller footprint on the NPU. 

|memo| **NOTE**: This is the recommended configuration and it should be used for most situations and by most applications.

To select this configuration, set the following environment variables based on your PC APU type:

For STX/KRK APUs:

.. code-block::

   set XLNX_VART_FIRMWARE=%RYZEN_AI_INSTALLATION_PATH%/voe-4.0-win_amd64/xclbins/strix/AMD_AIE2P_Nx4_Overlay.xclbin
   set XLNX_TARGET_NAME=AMD_AIE2P_Nx4_Overlay


For PHX/HPT APUs:

.. code-block::

   set XLNX_VART_FIRMWARE=%RYZEN_AI_INSTALLATION_PATH%/voe-4.0-win_amd64/xclbins/phoenix/1x4.xclbin
   set XLNX_TARGET_NAME=AMD_AIE2_Nx4_Overlay


Benchmark Configuration
=======================

The benchmark configuration maximizes NPU hardware resource usage, resulting in a larger footprint on the NPU. It is optimized for applications requiring high throughput and low latency from a single inference session.

|memo| **NOTE**: This configuration should only be used for testing Early Access features and for benchmarking purposes. Windows Studio Effects should be disabled when using this profile. To disable Windows Studio Effects, open Settings > Bluetooth & devices > Camera, select your primary camera, and then disable all camera effects.

To select this configuration, set the following environment variables based on your PC APU type:

For STX/KRK APUs:

.. code-block::

   set XLNX_VART_FIRMWARE=%RYZEN_AI_INSTALLATION_PATH%/voe-4.0-win_amd64/xclbins/strix/AMD_AIE2P_4x4_Overlay.xclbin
   set XLNX_TARGET_NAME=AMD_AIE2P_4x4_Overlay


For PHX/HPT APUs:

.. code-block::

   set XLNX_VART_FIRMWARE=%RYZEN_AI_INSTALLATION_PATH%/voe-4.0-win_amd64/xclbins/phoenix/4x4.xclbin
   set XLNX_TARGET_NAME=AMD_AIE2_4x4_Overlay



.. _config-file:

**************************
Runtime Configuration File
**************************

The Vitis AI Execution Provider (VAI EP) requires a runtime configuration file. A default version of this runtime configuration file can be found in the Ryzen AI Software installation tree: :file:`%RYZEN_AI_INSTALLATION_PATH%\\voe-4.0-win_amd64\\vaip_config.json`. 

It is required to create a copy of the :file:`vaip_config.json` file in your project directory and use this copy when initializing the inference session. The Vitis AI EP and the runtime configuration file used by the application must be taken from the same Ryzen AI Software release package. Refer to the :doc:`modelrun` page for more details on how to set up an inference session with the Vitis AI EP.

