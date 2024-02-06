NPU Management Interface
========================

Ryzen-AI features an integrated NPU utility tool called ``xbutil``, which is a command-line interface for both developers and end-users to monitor and manage the NPU. This feature is currently in the early access phase. 

The ``xbutil`` command-line tool can be accessed from ``C:\Windows\System32\AMD``. Within the Ryzen-AI installer conda environment, ``xbutil`` can be directly invoked.

Currently, it supports three primary commands:

- **examine:** Retrieves reports related to the Ryzen-AI Software Plaform and NPU.
- **validate:** Executes sanity tests on the NPU.
- **configure:** Manages the performance level of the NPU.

You can use ``--help`` with any command, such as ``xbutil examine --help``, to view all supported subcommands and their details.

1. Examining Ryzen-AI Software Platform and NPU Reports - Examples
------------------------------------------------------------------

- Provides OS/system information of the AI PC and informs about the presence of the NPU.

  .. code-block:: shell

     xbutil examine

- Provides more detailed information about the NPU, such as its architecture and performance mode.

  .. code-block:: shell

     xbutil examine -d --report platform

- Provides information about the NPU Binary loaded during model inference.

  .. code-block:: shell

     xbutil examine -d --report dynamic-regions

- Provides information about the column occupancy on the NPU, allowing you to determine if more models can run in parallel.

  .. code-block:: shell

     xbutil examine -d --report aie-partition

2. Executing Sanity Check on the NPU - Examples
------------------------------------------------

- Runs a built-in test on the NPU to ensure it is in a deployable state.

  .. code-block:: shell

     xbutil validate -d --run verify

3. Managing the Performance Level of the NPU - Examples
---------------------------------------------------------

- Sets the performance level of the NPU. You can choose powersaver mode, balanced mode, performance mode, or use the default.

  .. code-block:: shell

     xbutil configure -d --performance <powersaver | balanced | performance | default>

