#####################
Early Access Features
#####################

Early Access features are features which are still undergoing some optimization and fine-tuning. These features are not in their final form and may change as we continue to work in order to mature them into full-fledged features.


Ryzen AI Gen AI (LLM) Flow
~~~~~~~~~~~~~~~~~~~~~~~~~~

In Ryzen AI LLM flow, also known as the eager mode flow, the model deployed on the NPU through an operator-by-operator basis instead of compiling a complete graph. Specific compute-intensive operations, such as matrix multiplication based on GEMM/MATMUL operators, are dynamically offloaded to the NPU. The remaining operators are executed on the CPU. This approach simplifies the model ingestion process, reduces CPU load, and enables power savings on laptops. The latest state-of-the-art LLM models, such as OPT or Llama2, can be executed on a Ryzen AI-enabled laptop using the eager mode flow. 

The LLM eager mode flow consists of the following steps:

- **Quantize the pre-trained model**: For LLMs, it is often beneficial to employ a combination of SmoothQuant or AWQ (applied to the pre-trained PyTorch model) and/or dynamic quantization (utilizing ONNXRuntime ORTQuantizer) techniques to preserve accuracy as much as possible. As specific operators, like MATMUL, are offloaded to the NPU in the eager mode flow, it is also recommended to perform operator-specific quantization to quantize only the necessary operators.

- **Run the quantized model with ONNX Runtime Vitis AI execution provider**: The quantized model is executed using the ONNX Runtime and the Vitis AI execution provider. In addition to the NPU binary and the Vitis AI EP configuration file, the eager mode requires a library of instructions (in the form of a precompiled DLL) to run those quantized operators on the NPU. 

An example showing the OPT-1.3B model running on the NPU in eager mode can be found `here <https://github.com/amd/RyzenAI-SW/tree/main/example/transformers/opt-onnx>`_


Whisper-base Preview
~~~~~~~~~~~~~~~~~~~~

Preview example demonstrating Whisper-base running on the NPU are available on the Ryzen AI SW Early Access Secure Site. Access to the secure site can be requested here: 

https://account.amd.com/en/member/ryzenai-sw-ea.html.


NPU Management Interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Ryzen AI introduces ``xbutil``, an integrated utility tool to monitor and manage the NPU. It can be accessed from ``C:\Windows\System32\AMD`` and offers three primary commands: ``examine``, ``validate``, and ``configure``. Read more about ``xbutil`` `here <xbutil.html>`_.


