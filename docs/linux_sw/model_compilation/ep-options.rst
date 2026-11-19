Vitis AI EP Options
========================

The ``provider_options`` parameter configures the AMD Vitis™ AI Execution Provider when creating an ONNX Runtime InferenceSession. Pass these options as a dictionary to the ``provider_options`` parameter, as shown in the :doc:`compiling` examples.

The Vitis AI EP supports the following options, organized by category:

Required Options
----------------

These options must be provided when creating the InferenceSession.

config_file
~~~~~~~~~~~
Path to the JSON configuration file containing compilation options. This file specifies device configuration, optimization settings, and other compiler parameters. For complete details on configuration file structure and available options, see :doc:`ep-config-file`.

- **Type:** String
- **Required:** Yes

target
~~~~~~
Target platform for the Vitis AI Execution Provider.

- **Type:** String
- **Required:** Yes
- **Supported values:** "VAIML"

**Minimal example with required options:**

.. code-block:: python

    provider_options = {
        "config_file": "vitisai_config.json",
        "target": "VAIML"
    }

Caching Options (Recommended)
------------------------------

These options control where compiled model binaries are stored. Setting these options is recommended to ensure compiled models are cached in a predictable location and can be reused across sessions, avoiding recompilation.

cache_dir
~~~~~~~~~
Path to the directory where compiled model binaries are cached. When specified, the Vitis AI EP stores the compiled model in this directory. On subsequent runs with the same model, the cached binary is loaded instead of recompiling, significantly reducing startup time.

- **Type:** String
- **Default:** Current working directory

cache_key
~~~~~~~~~
Subfolder name within the cache directory for storing this specific compiled model. This allows multiple compiled models to coexist in the same cache directory without conflicts. Useful when compiling different models or the same model with different configurations.

- **Type:** String
- **Default:** Input ONNX model filename without extension

**Example with caching options:**

.. code-block:: python

    provider_options = {
        "config_file": "vitisai_config.json",
        "target": "VAIML",
        "cache_dir": "/path/to/cache",
        "cache_key": "my_model_v1"
    }

Analysis and Debugging Options
-------------------------------

These options generate analysis data for debugging and performance optimization. They are intended for short development and analysis sessions only. Profiling adds memory and performance overhead and should be avoided for long-running sessions. Do not enable these options in production deployment.

ai_analyzer_visualization
~~~~~~~~~~~~~~~~~~~~~~~~~
Enables generation of compile-time analysis data for visualizing model partitioning, operator placement decisions, and compilation flow. The output helps you understand how the compiler distributes operations between NPU and CPU.

- **Type:** Boolean
- **Default:** False

ai_analyzer_profiling
~~~~~~~~~~~~~~~~~~~~~
Enables generation of runtime profiling data for analyzing inference performance metrics, including execution time per operator and memory usage patterns.

- **Type:** Boolean
- **Default:** False

**Example with analysis options:**

.. code-block:: python

    provider_options = {
        "config_file": "vitisai_config.json",
        "target": "VAIML",
        "cache_dir": "/path/to/cache",
        "ai_analyzer_visualization": True,
        "ai_analyzer_profiling": True
    }

.. note::

   Analysis and profiling options increase compilation time and add memory and performance overhead at runtime. Use them only for short development and analysis runs—not for long-running sessions or production deployment.
