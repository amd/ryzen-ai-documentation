==================
Model Deployment
==================

This tutorial demonstrates the steps for deploying a ResNet50 model using Windows ML.
How to convert, compile, and deploy models in both Python and C++ environments.

****************
Model Conversion
****************

Model conversion is the first step in preparing your model for deployment with Windows ML.
You can use the AI Toolkit to convert models to the ONNX format and apply quantization.
- See the :doc:`model_conversion` page for details on model conversion using AI Toolkit.

*****************
Python Deployment
*****************

This section covers how to compile and deploy your ONNX model using Python.

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
        # For some EPs, there might not be a compilation output.
        # In that case, use the original model directly.
        output_model_path = input_model_path

Model Deployment
~~~~~~~~~~~~~~~~

Once the model is compiled, you can run inference using ONNX Runtime in Python.
This allows you to quickly validate model performance on your target hardware.
- Run the compiled model using an ORT session:

.. code-block:: bash

    python run_inference.py

Sample Output
~~~~~~~~~~~~~

The following is a sample output showing the top-5 predictions from the model.
You should see class indices and their associated confidence scores.

.. code-block:: bash

    285, Egyptian cat with confidence of 0.904274
    281, tabby with confidence of 0.0620204
    282, tiger cat with confidence of 0.0223081
    287, lynx with confidence of 0.00119624
    761, remote control with confidence of 0.000487919

**************
C++ Deployment
**************

C++ deployment is recommended for production scenarios where performance and integration with native Windows applications are critical.
This section shows how to compile and deploy your model using C++ APIs

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

After compiling the model, you can build and run your C++ application to perform inference.
- Build the example application and run using the Visual Studio Developer Command Prompt:

.. code-block:: bash

    msbuild RunInference.sln -p:Configuration=Release -p:Platform=x64

- Run the compiled model using an ORT session:

.. code-block:: bash

    .\RunInference.exe

Sample Output
~~~~~~~~~~~~~

The output below shows the top-5 predictions from the C++ inference application.
You should see similar results as in the Python deployment section.

.. code-block:: bash

    285, Egyptian cat with confidence of 0.904274
    281, tabby with confidence of 0.0620204
    282, tiger cat with confidence of 0.0223081
    287, lynx with confidence of 0.00119624
    761, remote control with confidence of 0.000487919
