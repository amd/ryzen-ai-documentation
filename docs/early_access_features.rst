#####################
Early Access Features
#####################

Ryzen AI Eager Mode
~~~~~~~~~~~~~~~~~~~

In the eager mode flow, the Ryzen AI software offloads specific operators onto the IPU to leverage dedicated hardware (IPU) for compute-intensive operations, such as matrix multiplication using GEMM/MATMUL operators. This approach helps save CPU utilization, enabling power savings on laptops, while the remaining operators continue to run on the CPU in an eager mode execution flow. The latest state-of-the-art LLM models, such as OPT or Llama2, can be executed on a Ryzen AI enabled laptop using the eager mode flow. 

In ONNX Runtime, the eager mode flow consists of the following steps:

- **Quantize the pre-trained model**: For LLMs, it is often beneficial to employ a combination of SmoothQuant (applied to the pre-trained PyTorch model) and dynamic quantization (utilizing ONNXRuntime ORTQuantizer) techniques to preserve accuracy as much as possible. As specific operators, like MATMUL, are offloaded to the IPU in the eager mode flow, it is also recommended to perform operator-specific quantization to quantize only the necessary operators.

- **Run the quantized model with ONNX Runtime Vitis AI execution provider**: The quantized model is executed using ONNX Runtime and Vitis AI execution provider. The runtime flow requires IPU binary, Vitis AI EP configuration file, and IPU instructions (precompiled DLL file) to run those quantized operators on the IPU. 


ONNX End-to-End Flow
~~~~~~~~~~~~~~~~~~~~

The ONNX end-to-end flow provides a framework to create and add pre/post-processing operators to the pre-trained model which enables end-to-end model inference using Vitis AI Execution Provider. The feature is built by leveraging the ONNX Runtime feature `ONNXRuntime-Extensions <https://onnxruntime.ai/docs/extensions/>`_. Typical pre-processing (or post-processing) tasks, such as resize, normalization, etc can be expressed as custom operators. The pretrained model can then be extended by absorbing these custom operators. The resulting model that contains the pre/post-processing operations can then be run on IPU. This helps improve end-to-end latency and facilitates PC power saving by reducing CPU utilization.

The model examples using ONNX end-to-end flow can be found <here:insert_link>

