#######################
Running LLMs on the NPU
#######################


The Ryzen AI Software includes support for deploying quantized LLMs on the NPU using an eager execution mode, simplifying the model ingestion process. Instead of compiling and executing as a complete graph, the model is processed on an operator-by-operator basis. Compute-intensive operations, such as GEMM/MATMUL, are dynamically offloaded to the NPU, while the remaining operators are executed on the CPU. 

A set of performance-optimized models is available upon request on the AMD secure download site: https://account.amd.com/en/member/ryzenai-sw-ea.html 

- Applicability: benchmarking and deployment of specific LLMs 
- Performance: highly optimized 
- Supported platforms: STX (and onwards) 
- Supported frameworks: ONNX Runtime GenAI 
- Supported models: Llama2, Llama3, Qwen1.5 


A general-purpose flow can be found here: https://github.com/amd/RyzenAI-SW/blob/main/example/transformers/models/llm/docs/README.md 

- Applicability: prototyping and early development with a broad set of LLMs 
- Performance: functional support only, not to be used for benchmarking 
- Supported platforms: PHX, HPT, STX (and onwards) 
- Supported frameworks: Pytorch 
- Supported models: Many 




..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
