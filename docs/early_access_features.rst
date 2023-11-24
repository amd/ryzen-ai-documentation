#####################
Early Access Features
#####################

Ryzen-AI Eager Mode
~~~~~~~~~~~~~~~~~~~


In eager mode flow, Ryzen AI software offloads specific operators on the IPU to get the benefit of using dedicated hardware (IPU) for compute-intensive operations such as matrix multiplication using GEMM/MATMUL operators, thus saving CPU utilization and enabling laptop power saving, while running the rest of the operators on the CPU in an eager mode execution flow. The latest state-of-the-art LLM models such as OPT or Llama2 can be run on the Ryzen-AI enabled laptop using the eager mode flow.  



In ONNX Runtime the eager mode flow consists of the following steps

Quantize the pre-trained model: For LLMs, it is often beneficial to use a combination of SmoothQuant (performed on the pre-trained PyTorch model) and dynamic quantization (using ONNXRuntime ORTQuntizer) techniques to preserve the accuracy as much as possible. As specific operators (such as MATMUL) are offloaded to IPU in eager mode flow, it is also recommended to do operator-specific quantization to quantize only the necessary operators. 
Run the quantized model with ONNX Runtime Vitis AI execution provider: The quantized model is executed using ONNX Runtime and Vitis AI execution provider. The runtime flow requires IPU binary, Vitis AI EP configuration file, and IPU instructions (precompiled DLL file) to run those quantized operators on the IPU. 
