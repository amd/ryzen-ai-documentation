#############
Runtime Setup
#############

.. _ipu-selection:

*********************
NPU Profile Selection
*********************

The NPU can be configured for different execution profiles. It is required to explicitly select an NPU profile before running an application from a new environment. 

.. note::
   In this documentation, **"NPU"** is used in descriptions, while **"IPU"** is retained in the tool's language, code, screenshots, and commands. This intentional 
   distinction aligns with existing tool references and does not affect functionality. Avoid making replacements in the code.

Throughput Profile
==================

**IMPORTANT**: This is the default profile, and it should be used for all CNN-based applications.

The throughput profile allows concurrent execution of four inference sessions in parallel on the NPU, with a performance of up to two TOPS per session. These parallel inference sessions can be run from different processes or applications, meeting the performance requirements of most real-time applications (such as video conferencing use cases) using the throughput profile.

Up to four additional inference sessions can be executed through temporal sharing of the NPU resources and at the expense of TOPS per session. 

The Ryzen AI runtime automatically manages the scheduling of the parallel sessions, requiring no user intervention. When the maximum load is reached and no other sessions can be submitted to the NPU, new incoming sessions are directed to run on the CPU.

To select the throughput profile, set the following environment variable:

.. code-block::

   set XLNX_VART_FIRMWARE=C:\path\to\1x4.xclbin


The :file:`1x4.xclbin` file is located in the ``voe-4.0-win_amd64`` folder of the Ryzen AI Software installation package. 


Latency Profile
===============

**IMPORTANT**: This profile should only be used for testing Early Access features and for benchmarking purposes. Windows Studio Effects should be disabled when using this profile. To disable Windows Studio Effects, open **Settings > Bluetooth & devices > Camera**, select your primary camera, and then disable all camera effects.

The latency profile allocates the entire NPU for a single inference session, delivering a performance of up to 10 TOPS for the session. 

Up to seven additional inference sessions can be executed through temporal sharing of the NPU resources and at the expense of TOPS per session. 

The Ryzen AI runtime automatically manages the scheduling of the parallel sessions, requiring no user intervention. When the maximum load is reached and no other sessions can be submitted to the NPU, new incoming sessions are directed to run on the CPU.

To select the latency profile, set the two following environment variables:

.. code-block::

   set XLNX_VART_FIRMWARE=C:\path\to\4x4.xclbin
   set XLNX_TARGET_NAME=AMD_AIE2_4x4_Overlay

The :file:`4x4.xclbin` file is located in the ``voe-4.0-win_amd64`` folder of the Ryzen AI Software installation package. 

.. _config-file:

**************************
Runtime Configuration File
**************************

The Vitis AI Execution Provider (VAI EP) requires a runtime configuration file. A default version of this runtime configuration file can be found in the ``voe-4.0-win_amd64`` folder of the Ryzen AI Software installation package under the name :file:`vaip_config.json`. 

It is recommended to create a copy of the :file:`vaip_config.json` file in your project directory and point to this copy when initializing the inference session. Refer to the :doc:`modelrun` page for more details on how to set up an inference session with the Vitis AI Execution Provider.

