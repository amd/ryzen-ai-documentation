#############
Runtime Setup
#############

.. _NPU-selection:

*****************
APU Types
*****************

The Ryzen AI Software supports different types of NPU-enabled APUs. These APU types are referred to as PHX, HPT and STX. 

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


***************************
Selecting NPU Configuration 
***************************

NPU configuration selection is a mandatory step before running an application from a new environment. Currently, Ryzen AI software provides two distinct configurations with two binary (.xclbin) files.

The **standard configuration** is designed to minimize NPU hardware resource usage, featuring a smaller footprint on the NPU.

To select this configuration, set the following environment variables based on your PC APU type:

For STX APUs:

.. code-block::

   set XLNX_VART_FIRMWARE=%RYZEN_AI_INSTALLATION_PATH%/voe-4.0-win_amd64/xclbins/strix/AMD_AIE2P_Nx4_Overlay.xclbin
   set XLNX_TARGET_NAME=AMD_AIE2P_Nx4_Overlay
   set NUM_OF_DPU_RUNNERS=1


For PHX/HPT APUs:

.. code-block::

   set XLNX_VART_FIRMWARE=%RYZEN_AI_INSTALLATION_PATH%/voe-4.0-win_amd64/xclbins/phoenix/1x4.xclbin
   set XLNX_TARGET_NAME=AMD_AIE2_Nx4_Overlay
   set NUM_OF_DPU_RUNNERS=1


The **benchmark configuration** maximizes NPU hardware resource usage, resulting in a larger footprint on the NPU. It is optimized for applications requiring high throughput and low latency from a single inference session.

**Note**: This configuration should only be used for testing Early Access features and for benchmarking purposes. Windows Studio Effects should be disabled when using this profile. To disable Windows Studio Effects, open Settings > Bluetooth & devices > Camera, select your primary camera, and then disable all camera effects.

To select this configuration, set the following environment variables based on your PC APU type:

For STX APUs:

.. code-block::

   set XLNX_VART_FIRMWARE=%RYZEN_AI_INSTALLATION_PATH%/voe-4.0-win_amd64/xclbins/strix/AMD_AIE2P_4x4_Overlay.xclbin
   set XLNX_TARGET_NAME=AMD_AIE2P_4x4_Overlay
   set NUM_OF_DPU_RUNNERS=1


For PHX/HPT APUs:

.. code-block::

   set XLNX_VART_FIRMWARE=%RYZEN_AI_INSTALLATION_PATH%/voe-4.0-win_amd64/xclbins/phoenix/4x4.xclbin
   set XLNX_TARGET_NAME=AMD_AIE2_4x4_Overlay
   set NUM_OF_DPU_RUNNERS=1

Irrespective of the configuration selected, up to eight simultaneous inference sessions can be run. The runtime automatically schedules each inference session to maximize its performance. However, it is important to note that the performance of individual inference sessions can be impacted by the increasing number of inference sessions running on the NPU, along with the NPU configuration used, and the applications running the inference sessions.


.. _config-file:

**************************
Runtime Configuration File
**************************

The Vitis AI Execution Provider (VAI EP) requires a runtime configuration file. A default version of this runtime configuration file can be found in the Ryzen AI Software installation tree: :file:`%RYZEN_AI_INSTALLATION_PATH%\\voe-4.0-win_amd64\\vaip_config.json`. 

It is recommended to create a copy of the :file:`vaip_config.json` file in your project directory and point to this copy when initializing the inference session. Refer to the :doc:`modelrun` page for more details on how to set up an inference session with the Vitis AI Execution Provider.

