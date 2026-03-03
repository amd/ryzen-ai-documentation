=========================
Windows ML ResNet Example
=========================

This tutorial demonstrates how to deploy a ResNet model using Windows ML, covering the complete workflow for converting, quantizing, compiling, and deploying models in both Python and C++ environments.

This tutorial provides step-by-step instructions for deploying a ResNet model, demonstrating:

- Setup instructions to create the Python environment and install dependencies
- Download the ResNet ONNX model
- (Optional) Quantize the model using AI Toolkit to QDQ ONNX format for low precision inference
- Compile and run the model on NPU using ONNX Runtime with Vitis AI Execution Provider using Python/C++ code

******************
Setup Instructions
******************

The source code files can be downloaded from `this link <https://github.com/amd/RyzenAI-SW/tree/main/WinML/CNN>`_. Alternatively, you can clone the RyzenAI-SW repo and change the directory into "WinML".

.. code-block::

    git clone https://github.com/amd/RyzenAI-SW.git
    cd RyzenAI-SW/WinML/CNN/python

|

The NPU driver and Windows App SDK should be correctly installed, as described in :doc:`Windows ML Installation <winml_overview>`_.

.. code-block:: shell

    conda create -n winml_resnet python==3.11
    conda activate winml_resnet
    pip install -r .\requirements.txt


Check the installed `Windows Apps SDK` python package using the command below.

.. code-block:: shell

    conda list | findstr wasdk


This should print the install version of the `Windows App SDK` python package. Ensure that the version is 1.8.5 or later.

.. code-block:: shell

    wasdk-microsoft-windows-ai-machinelearning 1.8.260209005            pypi_0    pypi
    wasdk-microsoft-windows-applicationmodel-dynamicdependency-bootstrap 1.8.260209005            pypi_0    pypi

Ensure that the `Windows App SDK` version matches the python package or download the specific version from `Windows App SDK 1.8.5 <https://learn.microsoft.com/en-us/windows/apps/windows-app-sdk/downloads>`_.

****************
Model Conversion
****************

Model conversion is the first step in preparing your model for deployment with Windows ML.
You can use the AI Toolkit to convert models to the ONNX format and apply quantization.

- Model quantization is optional step that can help reduce model size and improve inference performance.
- Original float model can be passed through automatic BF16 conversion. For more details refer to `Model conversion <../model_quantization.rst>`_
- See the `VS Code AI Toolkit model conversion <https://code.visualstudio.com/docs/intelligentapps/modelconversion>`_ page for details on model conversion using AI Toolkit.

If skipping the model quantization, you can directly download the ResNet ONNX model using the script:

.. code-block:: shell

    python models/download_model.py


*****************
Python Deployment
*****************

This section covers how to compile and deploy ResNet ONNX model using Python script. You can choose to deploy either the original FP32 ONNX model or the quantized QDQ ONNX model.


Model Inference
~~~~~~~~~~~~~~~

Use the python script to run inference which compiles and runs the model on NPU using ONNX runtime with Vitis AI Execution provider.
If you are using quantized model specify the quantized model path e.g. `model\\model_a8w8.onnx` and if you are using original FP32 model specify the original model path e.g. `model\\resnet50.onnx`.

.. code-block:: bash

    python run_model.py --model ..\model\resnet50.onnx --image_path ..\images\dog.jpg --ep_policy NPU

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

Model Inference
~~~~~~~~~~~~~~~

Instructions to build the example application and run using the Visual Studio Developer Command Prompt:

.. code-block:: bash

    cd <RyzenAI-SW>\WinML\CNN\cpp\CppResnetBuildDemo\
    nuget.exe restore .\CppResnetBuildDemo.sln
    msbuild .\CppResnetBuildDemo.sln /p:Configuration=Release /m

After compiling the model, you can build and run your C++ application to perform inference.

.. code-block:: bash

    .\x64\Release\CppResnetBuildDemo.exe --model ..\..\model\resnet50.onnx --image_path ..\..\images\dog.jpg --ep_policy NPU

Sample Output
~~~~~~~~~~~~~

The output below shows the top-5 predictions from the C++ inference application.
You should see similar results as in the Python deployment section.

.. code-block:: bash

    Top Predictions:
    -------------------------------------------
    Label                           Confidence
    -------------------------------------------
    207,golden retriever                 52.86%
    852,tennis ball                       1.60%
    805,soccer ball                       0.62%
    208,Labrador retriever                0.61%
    238,Greater Swiss Mountain dog        0.42%
    -------------------------------------------
    ---------------------------------------------
    Time taken for 20 iterations: 0 seconds
    Avg time per iteration : 19 milliseconds


For more examples using Transformer and LLM models with Windows ML, refer to `Windows ML examples in RyzenAI-SW <https://github.com/amd/RyzenAI-SW/tree/main/WinML>`_.

..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
