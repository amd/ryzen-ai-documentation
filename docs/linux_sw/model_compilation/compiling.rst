Model Compilation
=================

You can compile the model by executing a Python script that initializes an ONNX Runtime (ORT) inference session with the desired model and the AMD Vitis™ AI Execution Provider (EP). This process enables the Vitis AI EP to build the model, generating the necessary binaries for execution on the NPU.

.. important::

   The input ONNX model must have static shapes. Dynamic shapes are not
   supported. Models that use FP16, MX6, or MX9 data types are not supported
   on Strix and other AIE2P devices.

Use the following code as a simple template to compile models for the NPU:

.. code-block:: python

    import onnxruntime

    onnx_model = ...           # ONNX model to be compiled

    provider_options_dict = {
        "config_file": ...,    # JSON config file for the Vitis AI compiler
        "cache_dir":   ...,    # Path to the cache directory
        "cache_key":   ...,    # Subfolder in the cache directory for the compiled model
        "target":   ...,       # Target platform for Vitis AI execution provider
    }

    session = onnxruntime.InferenceSession(
        onnx_model,
        providers=["VitisAIExecutionProvider"],  # Use the Vitis AI Execution Provider
        provider_options=[provider_options_dict] # The provider options for the Vitis AI EP
    )


.. _supported-devices-for-compilation:

Supported Devices for Compilation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The compiler targets ``stx`` by default, which is required for all AIE2P devices.
You do not need to specify the device in the Vitis AI config file. A minimal
config file looks like this:

.. code-block:: json5

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
          "pass": ["init", "vaiml_partition"]
        }
      ]
    }

Device Configuration Options
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

VitisAI is available on Ryzen AI based devices:

- Ryzen AI 300 Series (Krackan Point and Strix Point)
- Ryzen AI Max / Max+ 300 Series (Strix Halo)
  
.. list-table::
   :header-rows: 1
   :widths: 30 50

   * - Device
     - Target Device
   * - Krackan Point, Strix Point, and Strix Halo
     - ``stx`` (default; no configuration required)


.. note::

    For ONNX models greater than 2GB and when converting a PyTorch model to ONNX format, the ONNX model can be split into 2 parts:

    - model.onnx
    - model.onnx.data

.. code-block:: python

    import onnxruntime
    import os

    Model = 'mymodel'

    # Prepend full path to ONNX model
    model_name = os.getcwd() + '/' + Model + '.onnx'
    compile_cache = os.getcwd() + '/cache_dir'

    provider_options_dict1 = {
        "config_file": 'vitisai_config.json',
        "cache_dir": compile_cache,
        "cache_key": Model,
        "ai_analyzer_visualization": True,  # Enable visualization output for analysis
        "ai_analyzer_profiling": True,      # Enable profiling data collection
        "target": "VAIML"
    }

    session1 = onnxruntime.InferenceSession(
        model_name,
        providers = ["VitisAIExecutionProvider"],
        provider_options = [provider_options_dict1])


Invoke the compiler to process the ONNX model with Vitis AI compiler:

   .. code-block:: bash

      python3 compile.py

 ``compile.py`` creates an ONNX Runtime inference session using the
 ``VitisAIExecutionProvider``. It reads compilation settings, such as the
 optimization level, from ``vitisai_config.json``. Running this script triggers model compilation and saves
 the compiled artifacts to the cache directory specified in the
 provider options.
