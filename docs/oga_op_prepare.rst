#######################################
Compiling Operators for OGA/ONNX Models
#######################################

Ryzen AI currently supports many popular LLMs in both hybrid and NPU-only flows. For these models, the required operators are already compiled and included in the Ryzen AI runtime. Such models can be run directly on Ryzen AI without any additional preparation.

When users fine-tune these models, only the weights change and no new operator shapes are introduced. In that case, follow the Model Preparation steps to prepare the model, which will run on the Ryzen AI runtime using the precompiled operators.

However, in cases where architectural changes introduce new operator shapes not available in the Ryzen AI runtime, additional operator compilation is required. This page provides a recipe to compile operators that are not already present in the runtime. **This flow is experimental, and results may vary depending on the extent of the architectural changes**.

All OGA models are currently based on the ONNX Runtime GenAI Model Builder (https://github.com/microsoft/onnxruntime-genai/tree/main/src/python/py/models#current-support) architecture. Therefore, this operator compilation flow assumes the models are supported by ONNX Runtime GenAI (or a close variant).

Operator Compilation Flow (Hybrid Execution)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Currently this flow is primarily supported for hybrid execution.

1. Ensure the model is quantized following the `quantization recipe <https://ryzenai.docs.amd.com/en/latest/oga_model_prepare.html#quantization>`_

2. Build the OGA DML model using the ONNX Runtime GenAI Model Builder included in the Ryzen AI software environment:

.. code-block:: 

   conda activate ryzen-ai-1.6.0
   python -m onnxruntime_genai.models.builder \
        -i <quantized model folder> -o <dml model folder> \
        -p int4 -e dml

3. Compile the operators extracted from the OGA DML model:

.. code-block::

   onnx_utils vaiml --model-dir <dml model folder> --plugin_name <plugin name> --compile --ops_type bfp16


This generates a compiled operator package at: ``transaction-plugin\<plugin name>.zip``. 

4. Generate the hybrid model:

Create a folder named ``dd_plugins`` in the current working directory and place ``<plugin name>.zip`` inside it. By default, the flow looks for the operator zip in ``dd_plugins``. To use a different location, see "Additional Details" below. 

Generate the hybrid model:

.. code-block:: 

    model_generate --hybrid <output hybrid model folder> <dml model folder>  

5. Run the hybrid model

Follow `official guide <https://ryzenai.docs.amd.com/en/develop/hybrid_oga.html#c-program>`_ to copy ``model_benchmark.exe`` and required DLL dependencies to the current working directory. Then run:

.. code-block::

   .\model_benchmark.exe -i <hybrid_model_folder> -f amd_genai_prompt.txt -l "128, 256, 512, 1024, 2048" --verbose

**Additional Details**

1. Path to operator zip file

If ``<plugin name>.zip`` is not placed in the ``dd_plugins`` folder, set the ``DD_PLUGINS_ROOT`` environment variable to point to its location:

.. code-block::

    set DD_PLUGINS_ROOT=C:\<path\to\folder\containing\<plugin name>.zip>

2. Enabling tracing

To enable tracing for debug purposes, set the ``DD_PLUGINS_TRACING`` environment variable before generating the hybrid model:

.. code-block::

   # Optional: enable tracing
   set DD_PLUGINS_TRACING=1

   # Generate the model
   model_generate --hybrid <output hybrid model folder> <dml model folder>  

 

