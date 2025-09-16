################
Model Deployment
################

In this tutorial we will use ResNet50 as an example to show different steps in Windows ML

****************
Model Conversion
****************

- Refer to :doc:`model_conversion` page for details on model conversion using AI Toolkit

*****************
Python Deployment
*****************

Model Compilation
~~~~~~~~~~~~~~~~~

.. code-block:: python

    input_model_path = "path_to_your_model.onnx"
    output_model_path = "path_to_your_compiled_model.onnx"

    model_compiler = ort.ModelCompiler(
        options,
        input_model_path,
        embed_compiled_data_into_model=True,
        external_initializers_file_path=None,
    )
    model_compiler.compile_to_file(output_model_path)
    if not os.path.exists(output_model_path):
        # For some EP, there might not be a compilation output.
        # In that case, use the original model directly.
        output_model_path = input_model_path


Model Deployment
~~~~~~~~~~~~~~~~

- Run the compiled model using ORT session

.. code-block:: python

    python run_inference.py


Sample Output
~~~~~~~~~~~~~

.. code-block:: bash

    285, Egyptian cat with confidence of 0.904274
    281, tabby with confidence of 0.0620204
    282, tiger cat with confidence of 0.0223081
    287, lynx with confidence of 0.00119624
    761, remote control with confidence of 0.000487919

**************
C++ Deployment
**************

Model Compilation
~~~~~~~~~~~~~~~~~

.. code-block:: c++

    const OrtCompileApi* compileApi = ortApi.GetCompileApi();

    // Prepare compilation options
    OrtModelCompilationOptions* compileOptions = nullptr;
    OrtStatus* status = compileApi->CreateModelCompilationOptionsFromSessionOptions(env, sessionOptions, &compileOptions);
    status = compileApi->ModelCompilationOptions_SetInputModelPath(compileOptions, modelPath.c_str());
    status = compileApi->ModelCompilationOptions_SetOutputModelPath(compileOptions, compiledModelPath.c_str());

    // Compile the model
    status = compileApi->CompileModel(env, compileOptions);

    // Clean up
    compileApi->ReleaseModelCompilationOptions(compileOptions);


Model Deployment
~~~~~~~~~~~~~~~~

- Build the example application and run using VS studio command prompt

.. code-block:: bash

    msbuild RunInference.sln -p:Configuration=Release -p:Platform=x64

- Run the compiled model using ORT session

.. code-block:: bash

    .\RunInference.exe


Sample Output
~~~~~~~~~~~~~

.. code-block:: bash

    285, Egyptian cat with confidence of 0.904274
    281, tabby with confidence of 0.0620204
    282, tiger cat with confidence of 0.0223081
    287, lynx with confidence of 0.00119624
    761, remote control with confidence of 0.000487919
