#####################
Early Access Features
#####################

Early Access features are features which are still undergoing some optimization and fine-tuning. These features are not in their final form and may change as we continue to work in order to mature them into full-fledged features.


Ryzen AI Eager Mode
~~~~~~~~~~~~~~~~~~~

In the eager mode, the Ryzen AI Software evaluates the model on an operator-by-operator basis instead of compiling a complete graph. Specific compute-intensive operations, such as matrix multiplication based on GEMM/MATMUL operators, are dynamically offloaded to the NPU. The remaining operators are executed on the CPU. This approach simplifies the model ingestion process, reduces CPU load and enables power savings on laptops. The latest state-of-the-art LLM models, such as OPT or Llama2, can be executed on a Ryzen AI enabled laptop using the eager mode flow. 

The eager mode flow consists of the following steps:

- **Quantize the pre-trained model**: For LLMs, it is often beneficial to employ a combination of SmoothQuant (applied to the pre-trained PyTorch model) and dynamic quantization (utilizing ONNXRuntime ORTQuantizer) techniques to preserve accuracy as much as possible. As specific operators, like MATMUL, are offloaded to the NPU in the eager mode flow, it is also recommended to perform operator-specific quantization to quantize only the necessary operators.

- **Run the quantized model with ONNX Runtime Vitis AI execution provider**: The quantized model is executed using the ONNX Runtime and the Vitis AI execution provider. In addition to the NPU binary and the Vitis AI EP configuration file, the eager mode requires a library of instructions (in the form of a precompiled DLL) to run those quantized operators on the NPU. 

An example showing the OPT-1.3B model running on the NPU in eager mode can be found `here <https://github.com/amd/RyzenAI-SW/tree/main/example/transformers/opt-onnx>`_


ONNX End-to-End Flow
~~~~~~~~~~~~~~~~~~~~

The ONNX end-to-end flow provides a framework to create and add pre/post-processing operators to the pre-trained model which enables end-to-end model inference using Vitis AI Execution Provider. The feature is built by leveraging the ONNX Runtime feature `ONNXRuntime-Extensions <https://onnxruntime.ai/docs/extensions/>`_. Typical pre-processing (or post-processing) tasks, such as resize, normalization, etc can be expressed as custom operators. The pretrained model can then be extended by absorbing these custom operators. The resulting model that contains the pre/post-processing operations can then be run on NPU. This helps improve end-to-end latency and facilitates PC power saving by reducing CPU utilization.

An example showing the ONNX end-to-end flow can be found `here <https://github.com/amd/RyzenAI-SW/tree/main/example/onnx-e2e>`_ 


Llama2 and Whisper-base Preview
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Preview examples demonstrating Llama2 and Whisper-base running on the NPU are available on the Ryzen AI SW Early Access Secure Site. Access to the secure site can be requested here: 

https://account.amd.com/en/member/ryzenai-sw-ea.html


NPU Management Interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ryzen AI introduces xbutil, an integrated NPU utility tool in early access. Accessed from C:\Windows\System32\AMD, it offers three commands—examine for reports, validate for sanity tests, and configure for NPU performance management—accessible through the command line within the Ryzen AI installer conda environment. Read more about the tool `here <xbutil.rst>`_



