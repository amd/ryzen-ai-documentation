Running the Compiled Model
==========================

The compiled model is deployed on the hardware board using ONNX Runtime with the AMD
Vitis AI Execution Provider (Vitis AI EP). The original ONNX model is loaded in an ONNX
Runtime inference session, and the Vitis AI EP dispatches the supported subgraphs to the
NPU while the remaining subgraphs fall back to the CPU execution provider at run time.

Files Needed on the Hardware Board
----------------------------------

The compilation phase produces the compiled model in one of two forms:

- A ``.rai`` file, which is the default output and packages the compiled model in a single
  file.
- A compiled cache directory, which holds the compiled model and the generated runtime
  shared libraries.

Either form can be copied to any folder on the Linux filesystem of the HW board.

To run the model on the hardware board, the following files are needed:

- The ``.rai`` file or the compiled cache directory
- The original ONNX model
- The JSON config file used to compile the model
- A Python script or C++ application to run the model

Deploying with ONNX Runtime and the Vitis AI Execution Provider
--------------------------------------------------------------------------

Just like model compilation, model inference is performed using an ONNX Runtime (ORT)
inference session.

The ORT inference session should be initialized as follows:

- The AMD Vitis AI Execution Provider must be used; otherwise, the model runs on the
  local CPU.
- The ONNX model should be the same as the one used during the compilation phase.
- The ``config_file`` provider option should point to the same configuration file as the
  one used during the compilation phase.
- The ``cache_dir`` and ``cache_key`` provider options should point to the compiled cache
  directory. These settings do not have to match the ones used during compilation. The
  compiled model can be placed in any folder on the Linux filesystem of the HW board. The
  combination of ``cache_dir/cache_key`` should simply point to this folder.

If the input ONNX model does not match the compiled model, or if the Vitis AI EP cannot
find the compiled model, the model is not deployed on the NPU.

If the input ONNX model matches the compiled model, the Vitis AI EP loads the compiled
model and is ready to deploy it on the NPU.

Once the ORT inference session is initialized, the model is deployed using the ORT session
``run`` API. For more information about the ONNX Runtime API, refer to the
`online documentation <https://onnxruntime.ai/docs/api/python/api_summary.html>`_.

Upon execution, the subgraphs containing operators supported by the NPU are executed on
the NPU by the Vitis AI EP. The remaining subgraphs are executed on the CPU.

The following code can be used as a simple template to deploy models on the NPU:

.. code-block:: python

    import onnxruntime

    onnx_model = ...        # Original ONNX model used during the compilation phase

    provider_options_dict = {
        "config_file": ..., # Original JSON config file during the compilation phase
        "cache_dir":   ..., # Path to the cache directory
        "cache_key":   ..., # Subfolder in the cache directory with the compiled model
        "target":   ...,    # Target platform for Vitis AI execution provider
    }

    # Create the ORT inference session
    session = onnxruntime.InferenceSession(
        onnx_model,
        providers=["VitisAIExecutionProvider"],
        provider_options=[provider_options_dict]
    )

    # Initialize input tensors
    input_data = {}
    for input in session.get_inputs():
        input_data[input.name] = ...

    # Run model
    outputs = session.run(None, input_data)

