#############
Runtime Setup
#############

.. _NPU-selection:

*****************
APU Types
*****************

The Ryzen AI Software supports different types of NPU-enabled APUs. These APU types are referred to as PHX, HPT and STX. 

To determine the type of the local APU, it is possible to check the ``HKEY_LOCAL_MACHINE\HARDWARE\DESCRIPTION\System\CentralProcessor\0\Identifier`` value in the Windows Registry.

.. list-table:: 
   :widths: 30 30 40 
   :header-rows: 1

   * - Family Number
     - Model Number
     - APU Type
   * - 0x19
     - 0x70 - 0x7F
     - PHX or HPT 
   * - 0x1A
     - 0x30 - 0x3F
     - STX



*********************
NPU Profile Selection
*********************

The NPU can be configured for different execution profiles. It is required to explicitly select an NPU profile before running an application from a new environment. 


Throughput Profile
==================

The throughput profile allows concurrent execution of four inference sessions in parallel on the NPU, with a performance of up to two TOPS per session. These parallel inference sessions can be run from different processes or applications, meeting the performance requirements of most real-time applications (such as video conferencing use cases) using the throughput profile.

Up to four additional inference sessions can be executed through temporal sharing of the NPU resources and at the expense of TOPS per session. 

The Ryzen AI runtime automatically manages the scheduling of the parallel sessions, requiring no user intervention. When the maximum load is reached and no other sessions can be submitted to the NPU. 

To select the throughput profile, set the following environment variables based on your APU type:

For STX APUs:

.. code-block::

   set XLNX_VART_FIRMWARE=%RYZEN_AI_INSTALLATION_PATH%/voe-4.0-win_amd64/xclbins/strix/AMD_AIE2P_Nx4_Overlay.xclbin
   set NUM_OF_DPU_RUNNERS=1


For PHX/HPT APUs:

.. code-block::

   set XLNX_VART_FIRMWARE=%RYZEN_AI_INSTALLATION_PATH%/voe-4.0-win_amd64/xclbins/phoenix/1x4.xclbin
   set NUM_OF_DPU_RUNNERS=1



Latency Profile
===============

**IMPORTANT**: This profile should only be used for testing Early Access features and for benchmarking purposes. Windows Studio Effects should be disabled when using this profile. To disable Windows Studio Effects, open **Settings > Bluetooth & devices > Camera**, select your primary camera, and then disable all camera effects.

The latency profile allocates the entire NPU for a single inference session, delivering a performance of up to 10 TOPS for the session. 

Up to seven additional inference sessions can be executed through temporal sharing of the NPU resources and at the expense of TOPS per session. 

The Ryzen AI runtime automatically manages the scheduling of the parallel sessions, requiring no user intervention. When the maximum load is reached and no other sessions can be submitted to the NPU.

To select the latency profile, set the following environment variables based on your APU type:

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


.. _config-file:

**************************
Runtime Configuration File
**************************

The Vitis AI Execution Provider (VAI EP) requires a runtime configuration file. A default version of this runtime configuration file can be found in the Ryzen AI Software installation tree: :file:`%RYZEN_AI_INSTALLATION_PATH%\\voe-4.0-win_amd64\\vaip_config.json`. 

It is recommended to create a copy of the :file:`vaip_config.json` file in your project directory and point to this copy when initializing the inference session. Refer to the :doc:`modelrun` page for more details on how to set up an inference session with the Vitis AI Execution Provider.

