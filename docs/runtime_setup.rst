#############
Runtime Setup
#############

.. _ipu-selection:

*********************
IPU Profile Selection
*********************


The IPU can be configured for different execution profiles. It is required to explicitly select an IPU profile before running an application from a new environment. 


Throughput Profile
==================

The throughput profile allows running 4 inference sessions in parallel on the IPU, with a performance of up to 2 TOPS per session. These parallel inference sessions can be run from different processes or applications. The performance requirements of most real-time applications (such as video conferencing use cases) can be met using the throughput profile.

Up to 4 additional inference sessions can be executed through temporal sharing of the IPU resources and at the expense of TOPS per session. 

The Ryzen AI runtime automatically manages the scheduling of the parallel sessions. No user intervention is required. When the maximum load is reached and no other sessions can be submitted to the IPU, new incoming sessions are run on the CPU.

To select the throughput profile, set the following environment variable:

.. code-block::

   set XLNX_VART_FIRMWARE=C:\path\to\1x4.xclbin


Latency Profile
===============

The latency profile allocates the entire IPU for a single inference session, delivering a performance of up to 10 TOPS for that session. 

Up to 7 additional inference sessions can be executed through temporal sharing of the IPU resources and at the expense of TOPS per session. 

The Ryzen AI runtime automatically manages the scheduling of the parallel sessions. No user intervention is required. When the maximum load is reached and no other sessions can be submitted to the IPU, new incoming sessions are run on the CPU.

To select the latency profile, set the two following environment variables:

.. code-block::

   set XLNX_VART_FIRMWARE=C:\path\to\5x4.xclbin
   set XLNX_TARGET_NAME=AMD_AIE2_5x4_Overlay


.. _config-file:

**************************
Runtime Configuration File
**************************

The Execution Provider setup package contains the Vitis AI Execution Provider runtime configuration file :file:`vaip_config.json`. This file is required when configuring Vitis AI Execution Provider (VAI EP) inside the ONNX Runtime code.
