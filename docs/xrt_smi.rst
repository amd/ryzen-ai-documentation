NPU Management Interface
========================

.. note::
   This feature is currently in the Early Access stage. Early Access features are features which are still undergoing some optimization and fine-tuning. These features are not in their final form and may change as we continue to work in order to mature them into full-fledged features.


The ``xrt-smi`` utility is a command-line interface to monitor and manage the NPU.  It is an OS agnostic tool which supports devices from Edge to Cloud/DC and now NPU integrated AMD CPUs. 

It is installed in ``C:\Windows\System32\AMD`` and it can be directly invoked from within the conda environment created by the Ryzen AI Software installer.

The ``xrt-smi`` utility currently supports three primary commands:

- **examine:** Examines the state of the AI PC and the NPU.
- **validate:** Executes sanity tests on the NPU.
- **configure:** Manages the performance level of the NPU.


You can use ``--help`` with any command, such as ``xrt-smi examine --help``, to view all supported subcommands and their details. 

Both examine and validate support an additional option --format which takes JSON (``-f JSON``) and can be used to get JSON output (``-o <example.json>``) for automation purposes.

Examining the AI PC and the NPU
-------------------------------

- To provide OS/system information of the AI PC and informs about the presence of the NPU:

  .. code-block:: shell

     xrt-smi examine

  *Sample Command Line Output:*

  .. image:: images/examine.png

  To get output in JSON format:

  .. code-block:: shell

     xrt-smi examine -f JSON -o <specify path to create json file examine.json>

- To provide more detailed information about the NPU, such as its performance mode and clocks:

  .. code-block:: shell

     xrt-smi examine --report platform

  *Sample Command Line Output:*

  .. image:: images/report_platform.png

- To show details about the AIE/NPU partition, column occupancy on the NPU, allowing you to determine if more models can run in parallel:

  .. code-block:: shell

     xrt-smi examine --report aie-partitions

  *Sample Command Line Output:*

  .. image:: images/aie_partitions.png

- To show details about the AIE/NPU partition in another view of columns to HW context for better understanding:

  .. code-block:: shell

     xrt-smi examine --report aie-partitions --verbose

  *Sample Command Line Output:*

  .. image:: images/aie_partitions_verbose.png

- To show details about the opcode trace (stx) or stream buffer tokens (phx):

  .. code-block:: shell

     xrt-smi examine -r telemetry
  
  *Sample Command Line Output on Strix (STX):*

  .. image:: images/telemetry_stx.png

  *Sample Command Line Output on Phoenix (PHX):*

  .. image:: images/telemetry_phx.png


Executing a Sanity Check on the NPU
-----------------------------------

- To run a built-in test on the NPU to ensure it is in a deployable state. It runs all test in the suite for device validation, includes verify, df-bw, tct  and gemm tests

  .. code-block:: shell

     xrt-smi validate --run <all>

*Sample Command Line Output:*
    
  .. image:: images/validate.png


Managing the Performance Level of the NPU
-----------------------------------------

- To set the performance level of the NPU. You can choose powersaver mode, balanced mode, performance mode, or use the default:

  .. code-block:: shell

     xrt-smi configure --pmode <powersaver | balanced | performance | default>

  *Sample Command Line Output:*

  .. image:: images/configure_pmode.png

