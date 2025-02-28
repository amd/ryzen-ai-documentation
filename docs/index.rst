##########################
Ryzen AI Software   
##########################

AMD Ryzen™ AI Software includes the tools and runtime libraries for optimizing and deploying AI inference on AMD Ryzen™ AI powered PCs. Ryzen AI software enables applications to run on the neural processing unit (NPU) built in the AMD XDNA™ architecture, as well as on the integrated GPU. This allows developers to build and deploy models trained in PyTorch or TensorFlow and run them directly on laptops powered by Ryzen AI using ONNX Runtime and the Vitis™ AI Execution Provider (EP).

.. image:: images/rai-sw-1.3.png
   :align: center

***********
Quick Start
***********

- :ref:`Supported Configurations <supported-configurations>`
- :doc:`inst`
- :doc:`examples`

*************************
Development Flow Overview
*************************

The Ryzen AI development flow does not require any modifications to the existing model training processes and methods. The pre-trained model can be used as the starting point of the Ryzen AI flow.

Quantization
============
Quantization involves converting the AI model's parameters from floating-point to lower-precision representations, such as 16-bit or 8-bit integers. Quantized models are more power-efficient, utilize less memory, and offer better performance. 

**Quark** is a comprehensive cross-platform deep learning toolkit designed to simplify and enhance the quantization of deep learning models. Supporting both PyTorch and ONNX models, Quark empowers developers to optimize their models for deployment on a wide range of hardware backends, achieving significant performance gains without compromising accuracy.

For more details, refer to the :doc:`modelport` page.

Pre-optimized models can be found on the `Ryzen AI Model Zoo <https://huggingface.co/models?other=RyzenAI>`_ on Hugging Face.

Deployment
==========
The AI model is deployed using the ONNX Runtime with either C++ or Python APIs. The Vitis AI Execution Provider included in the ONNX Runtime intelligently determines what portions of the AI model should run on the NPU, optimizing workloads to ensure optimal performance with lower power consumption.

For more details, refer to the :doc:`modelrun` page.



|
|


.. toctree::
   :maxdepth: 1
   :hidden:

   relnotes.rst


.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Getting Started on the NPU

   inst.rst
   runtime_setup.rst
   examples.rst

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Running CNNs on the NPU

   modelcompat.rst
   modelport.rst
   modelrun.rst
   app_development.rst


.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Running Models on the GPU

   gpu/ryzenai_gpu.rst

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Running LLMs on the NPU

   llm/overview.rst
   llm/high_level_python.rst
   llm/server_interface.rst
   hybrid_oga.rst

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Additional Features

   xrt_smi.rst
   ai_analyzer.rst



.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Additional Topics

   Model Zoo <https://huggingface.co/models?other=RyzenAI>
   manual_installation.rst
   Licensing Information <licenses.rst>



..
  ------------
  #####################################
  License
  #####################################
  
  Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
