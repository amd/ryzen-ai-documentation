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


********************
NPU Binary Selection
********************

NPU binary selection is a mandatory step before running an application from a new environment. Currently, Ryzen AI software provides two distinct binary profiles: a "light" version and a "max" version, each optimized for different performance characteristics:

NPU Binary "Light" is designed to minimize NPU hardware resource usage, this binary has a smaller footprint on the NPU. This binary allows a greater number of applications to run on the NPU without any loss of performance for each application.

To select this binary, set the following environment variables based on your PC APU type:

For STX APUs:

.. code-block::

   set XLNX_VART_FIRMWARE=%RYZEN_AI_INSTALLATION_PATH%/voe-4.0-win_amd64/xclbins/strix/AMD_AIE2P_Nx4_Overlay.xclbin
   set NUM_OF_DPU_RUNNERS=1


For PHX/HPT APUs:

.. code-block::

   set XLNX_VART_FIRMWARE=%RYZEN_AI_INSTALLATION_PATH%/voe-4.0-win_amd64/xclbins/phoenix/1x4.xclbin
   set NUM_OF_DPU_RUNNERS=1


NPU Binary "Max" maximizes NPU hardware resource usage, resulting in a larger footprint on the NPU. It is optimized for application requiring high throughput and low latency from a single inference session.

To select this binary, set the following environment variables based on your PC APU type:

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

Irrespective of the binary selected, the NPU can handle a maximum of eight simultaneous inference sessions. The runtime automatically schedules each inference session to maximize performance. However, it is important to note that the performance of individual inference sessions can be impacted by the increasing number of inference sessions running on the NPU, along with the NPU hardware (depending on APU types), and the applications running the inference sessions.



**IMPORTANT**: NPU binary "Max" should only be used for testing Early Access features and for benchmarking purposes. Windows Studio Effects should be disabled when using this profile. To disable Windows Studio Effects, open **Settings > Bluetooth & devices > Camera**, select your primary camera, and then disable all camera effects.


.. _config-file:

**************************
Runtime Configuration File
**************************

The Vitis AI Execution Provider (VAI EP) requires a runtime configuration file. A default version of this runtime configuration file can be found in the Ryzen AI Software installation tree: :file:`%RYZEN_AI_INSTALLATION_PATH%\\voe-4.0-win_amd64\\vaip_config.json`. 

It is recommended to create a copy of the :file:`vaip_config.json` file in your project directory and point to this copy when initializing the inference session. Refer to the :doc:`modelrun` page for more details on how to set up an inference session with the Vitis AI Execution Provider.

