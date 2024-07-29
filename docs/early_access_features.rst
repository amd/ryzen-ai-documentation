#####################
Early Access Features
#####################

Early Access features are those that are still undergoing optimization and fine-tuning. These features are not in their final form and might change as we continue to refine them into fully developed features.


Suport for Generative AI
========================
"The latest version of Ryzen AI Software includes early access support for Generative AI (Gen AI), transformers, and LLMs. Like CNNs, Gen AI models require quantization before deployment on the NPU. However, the development flow for Gen AI models has some differences due to their distinct nature.

**Quantization:** For Gen AI models, it is often advantageous to use a combination of SmoothQuant or AWQ (applied to the pre-trained PyTorch model) and/or dynamic quantization (leveraging ONNXRuntime ORTQuantizer) techniques to maintain the highest possible accuracy. Because only specific operators are offloaded to the NPU, it is also recommended to conduct operator-specific quantization to selectively quantize necessary operators (typically GEMM/MATMUL).

**Deployment:** Gen AI models are deployed on the NPU using an eager execution mode, simplifying the model ingestion process. Instead of compiling and executing as a complete graph, the model is processed on an operator-by-operator basis. Compute-intensive operations, such as GEMM/MATMUL, are dynamically offloaded to the NPU, while the remaining operators are executed on the CPU. Eager mode for Gen AI models is supported in both PyTorch and the ONNX Runtime.

The following LLMs and transformers are supported and provided as examples:

- `Llama 2 with PyTorch <https://github.com/amd/RyzenAI-SW/tree/main/example/transformers>`_
- `OPT-1.3B with PyTorch <https://github.com/amd/RyzenAI-SW/tree/main/example/transformers/opt-pytorch>`_  
- `OPT-1.3B with ONNXRuntime <https://github.com/amd/RyzenAI-SW/tree/main/example/transformers/opt-onnx>`_  
-	Whisper base with ONNX Runtime (Access via Early Access secure site - `Request access here <https://account.amd.com/en/member/ryzenai-sw-ea.html>`_)

|
|

NPU Management Interface
========================
The ``xbutil`` utility is an integrated command-line interface to monitor and manage the NPU. For more details, click `here <xbutil.html>`_.


