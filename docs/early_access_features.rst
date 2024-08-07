##################
Generative AI Flow
##################

The latest version of Ryzen AI Software includes early access support for Generative AI, transformers, and LLMs. Like CNNs, Gen AI models require quantization before deployment on the NPU. However, the development flow for Gen AI models features some differences due to their distinct nature.

**Quantization:** For Gen AI models, it's often advantageous to use a combination of SmoothQuant or AWQ (applied to the pre-trained PyTorch model) and/or dynamic quantization (leveraging ONNXRuntime ORTQuantizer) techniques to maintain the highest possible accuracy. Since only specific operators are offloaded to the NPU, it's also recommended to conduct operator-specific quantization to selectively quantize necessary operators (typically GEMM/MATMUL).

**Deployment:** Gen AI models are deployed on the NPU using an eager execution mode, simplifying the model ingestion process. Instead of compiling and executing as a complete graph, the model is processed on an operator-by-operator basis. Compute-intensive operations, such as GEMM/MATMUL, are dynamically offloaded to the NPU, while the remaining operators are executed on the CPU. Eager mode for Gen AI models is supported in both PyTorch and the ONNX Runtime.

The following LLMs and transformers are supported and provided as examples:

- `Llama 2 with PyTorch <https://github.com/amd/RyzenAI-SW/tree/main/example/transformers>`_
- `OPT-1.3B with PyTorch <https://github.com/amd/RyzenAI-SW/tree/main/example/transformers>`_  
- `OPT-1.3B with ONNXRuntime <https://github.com/amd/RyzenAI-SW/tree/main/example/transformers>`_  

..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
