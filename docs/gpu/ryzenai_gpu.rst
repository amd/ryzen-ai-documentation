############
Ryzen AI GPU
############

With AMD Ryzen AI Software, AMD provides highly optimized DirectML implementation to run AI models on AMD iGPU and dGPU hardware. AMD collaborates closely with Microsoft to add capabilities and to optimize Microsoft DirectML framework running on top of AMD device driver resident ML layers to accelerate ML primitives on AMD GPUs.

Prerequisites
~~~~~~~~~~~~~

- DirectX12 capable Windows OS (Windows 11 recommended)
- Latest AMD `GPU device driver <https://www.amd.com/en/support>`_ installed
- `Microsoft Olive <https://microsoft.github.io/Olive/getstarted/installation.html#>`_ for model conversion and optimization
- Latest `ONNX Runtime DirectML EP <https://onnxruntime.ai/docs/execution-providers/DirectML-ExecutionProvider.html>`_ 

You can ensure GPU driver and DirectX version from ``Windows Task Manager`` -> ``Performance`` -> ``GPU`` 

Running models on Ryzen AI GPU
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Running model on Ryzen AI GPU can be summarized in a couple of easy steps: 

**Model Conversion and Optimization**: After the model is trained, if the model is not already in ONNX format, you can use Microsoft Olive Optimizer to convert your models to ONNX first and then optimize using Olive optimizer for optimal target execution.  

For Olive flow please refer to `Microsoft Olive Documentation <https://microsoft.github.io/Olive/>`_


**Deployment**: Once the model is in ONNX format, you deploy and run the model with ONNX Runtime DirectML EP (``DmlExecutionProvider``) to accelerate with AMD Ryzen AI GPU device. 


For DirectML related information please refer `DirectML documentation <https://onnxruntime.ai/docs/execution-providers/DirectML-ExecutionProvider.html>`_

 
Examples
~~~~~~~~

A simple model optimization and running example with ResNet: TBD 


