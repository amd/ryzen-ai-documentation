Examine, Validate, and Configure the NPU
=========================================
Ryzen-AI features an integrated NPU explorer tool called 'xbutil,' which is a command-line interface for both developers and end-users to monitor and manage the NPU. This feature is currently in the early access phase. Currently, it supports three primary commands:

- **examine:** Retrieves reports related to the platform and AIE.
- **validate:** Executes sanity tests on the device.
- **configure:** Manages the performance level of the device.

1. Examining Platform and AIE Reports Examples
------------------------------------------------

.. code-block:: shell

   xbutil examine
    
Provides OS/system information of the AI PC and informs about the presence of the NPU. 

.. code-block:: shell

   xbutil examine -d --report platform
 
Provides more detailed information about the NPU, such as its architecture and performance mode.

.. code-block:: shell

   xbutil examine -d --report dynamic-regions
 
Provides information about the NPU Binary loaded during model inference.

.. code-block:: shell

   xbutil examine -d --report aie-partition
 
Provides information about the column occupancy on the NPU, allowing you to determine if more models can run in parallel.

2. Executing Sanity Check on the NPU Examples
------------------------------------------------

.. code-block:: shell

   xbutil validate -d --run verify

Runs a built-in test on the NPU to ensure it is in a deployable state.

3. Managing the Performance Level of the NPU Examples
---------------------------------------------------------

.. code-block:: shell

   xbutil configure -d --performance <powersaver | balanced | performance | default>

Sets the performance level of the NPU. Your can choose powersaver mode or performance mode based on your preference. The default performance level is set to balanced.
