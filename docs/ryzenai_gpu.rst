############
Ryzen AI GPU
############

With AMD Ryzen AI Software, AMD provides highly optimized DirectML implementation to run AI models on AMD iGPU and dGPU hardware. AMD collaborates closely with Microsoft to add capabilities and to optimize Microsoft DirectML framework running on top of AMD device driver resident ML layers to accelerate ML primitives on AMD GPUs 

To use the above software stack, you will need to be on DirectX12 capable Windows OS and have the latest AMD GPU device drivers installed. No additional package is needed to run with the Ryzen AI GPU stack shown above, but it’s always recommended to use latest onnxruntime-directML package and latest AMD driver installed for best performance. 

Running models on Ryzen AI GPU
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Running model on Ryzen AI GPU can be summarized in couple of easy steps: 

**Model Conversion and Optimization**: After the model is trained, If your model is not already in ONNX format, you can use Microsoft Olive Optimizer to convert your models to ONNX first and then optimize using Olive optimizer for optimal target execution 

For Olive installation and optimization flow please refer to `Microsoft Olive Documentation <https://microsoft.github.io/Olive/>`_


**Deployment**: Once the model is in ONNX format, you deploy and run the model with ONNX Runtime DirectML execution provider (``DmlExecutionProvider``) to accelerate with AMD Ryzen AI GPU device. 


For DirectML Execution provider installation and more information please refer `DirectML documentation <https://onnxruntime.ai/docs/execution-providers/DirectML-ExecutionProvider.html>`_

 

