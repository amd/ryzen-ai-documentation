Vitis AI EP Configuration File
====================================

Provide a JSON configuration file using the ``config_file`` provider option when creating the ONNX Runtime inference session. The following example shows a typical configuration:

.. code-block:: json

    {
      "passes": [
       {
         "name": "init",
         "plugin": "vaip-pass_init"
       },
       {
        "name": "vaiml_partition",
        "plugin": "vaip-pass_vaiml_partition",
        "vaiml_config":
        {
          "optimize_level": 2
        }
       }
      ],
      "target": "VAIML",
      "targets": [
        {
            "name": "VAIML",
            "pass": [
                "init",
                "vaiml_partition"
            ]
        }
      ]
    }

All options in ``vaiml_config`` have defaults and can be omitted. See the individual option descriptions in the following sections for details on types, supported values, and defaults.

Configuration Options
---------------------

The following options can be specified in the ``vaiml_config`` section of the configuration file.

device
~~~~~~
The target device for compilation. It defaults to ``stx``, which is required for all AIE2P devices (Krackan Point, Strix Point, and Strix Halo). Do not specify this option in the configuration file.

optimize_level
~~~~~~~~~~~~~~

Controls the compiler's optimization level to balance performance, memory usage, and compile-time stability.

- **Type:** Integer
- **Supported values:** 2, 3
- **Default:** 2

.. code-block:: json

    "vaiml_config": {
      "optimize_level": 2
    }

Optimization Levels
^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 10 45 45

   * - Level
     - Description
     - Use Cases
   * - 2
     - Enables advanced optimizations including kernel chaining and efficient L2 memory allocation. Falls back to DDR (external memory) if the model overflows L2 memory (NPU Mem Tiles). Reduces latency and minimizes DDR traffic.
     - Production builds, models benefiting from kernel chaining optimizations
   * - 3
     - Instructs the compiler to apply more aggressive latency optimizations than level 2.
     - When a model fails to meet its latency targets with level 2. It is intended as a next-step option for squeezing out additional performance in latency-sensitive workloads.


**Important:** 3 is an Early Access (EA) option. As such, it might not be fully validated or production-ready, and it is recommended to use this option only when standard optimization paths have been exhausted.

**Note:** Kernel chaining combines multiple operations to reduce memory transfers. L2 memory refers to on-chip NPU memory tiles. DDR is external memory accessed when on-chip memory is insufficient.


Debugging Options
-----------------

The following options are for debugging only. Omit them from your configuration
file, and use them only when you need to investigate an unexpected compilation
or runtime failure.

logging_level
~~~~~~~~~~~~~

Controls the verbosity of compiler logging output.

- **Type:** String
- **Supported values:** "info", "warning", "error"
- **Default:** "error"

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Level
     - Description
   * - info
     - Details about significant events or actions, including comparative information between options
   * - warning
     - Recoverable issues and differences between options
   * - error
     - Critical failures that prevent program continuation (limited details)

**Example**

  .. code-block:: json

    "vaiml_config": {
          "logging_level": "info"
    }

keep_outputs
~~~~~~~~~~~~

Specifies whether to preserve intermediate compilation files or generate profiling files during execution for debugging.

- **Type:** Boolean
- **Supported values:** true, false
- **Default:** false

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Value
     - Description
   * - true
     - The Vitis AI compiler preserves both the <cache-dir>/<cache-key>/<model>.rai file and the complete vaiml directory structure.
   * - false
     - Only the <cache-dir>/<cache-key>/<model>.rai file is retained.
     
**Example**

  .. code-block:: json

    "vaiml_config": {
          "keep_outputs": true
    }

override_batch_size
~~~~~~~~~~~~~~~~~~~~

Configures static batching behavior for ONNX models. Static batching sets a
fixed batch size at model build or export time. Every inference request must
provide exactly this number of inputs; supplying a different number results in
an error. This approach is efficient, but the input batch size must remain
constant.

The compiler has limited support for static batch sizes greater than 1. If
compilation fails on such a model, set ``override_batch_size`` to force it to
compile as batch size 1.

**override_batch_size**:

- **Type:** Boolean
- **Description:** Forces a model with a static batch size greater than 1 to
  compile as batch size 1. Use this when compilation fails at the model's
  declared batch size.
- **Example:**

  .. code-block:: json

    "vaiml_config": {
       "override_batch_size": true
     }

- **Limitations:** Static batch sizes above 6 are not supported.
