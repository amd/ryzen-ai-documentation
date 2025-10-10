##########################
Ryzen AI Software
##########################

AMD Ryzen™ AI Software includes the tools and runtime libraries for optimizing and deploying AI inference on AMD Ryzen™ AI powered PCs. Ryzen AI software enables applications to run on the neural processing unit (NPU) built in the AMD XDNA™ architecture, as well as on the integrated GPU. This allows developers to build and deploy models trained in PyTorch or TensorFlow and run them directly on laptops powered by Ryzen AI using ONNX Runtime and the Vitis™ AI Execution Provider (EP).

.. image:: images/rai-sw.png
   :align: center

.. _hardware-support:
****************
Hardware Support
****************
Ryzen AI 1.6 Software runs on AMD processors outlined below. For a more detailed list of supported devices, refer to the `processor specifications <https://www.amd.com/en/products/specifications/processors.html>`_ page (scroll to the "AMD Ryzen™ AI" column toward the right side of the table, and select "Available" from the pull-down menu). Support for Linux is coming soon in Ryzen AI 1.6.1.

.. list-table:: Supported Ryzen AI Processor Configurations
   :header-rows: 1
   :widths: 25 25 12 22 12 10 10 10

   * - Series
     - Codename
     - Abbreviation
     - Graphics Model
     - Ryzen™ AI Support
     - Launch Year
     - Windows
     - Linux
   * - Ryzen AI Max PRO 300 Series
     - Strix Halo
     - STX
     - Radeon 8000S Series
     - ✅
     - 2025
     - ☑️
     - 
   * - Ryzen AI PRO 300 Series
     - Strix Point / Krackan Point
     - STX/KRK
     - Radeon 800M Series
     - ✅
     - 2025
     - ☑️
     - 
   * - Ryzen AI Max 300 Series
     - Strix Halo
     - STX
     - Radeon 8000S Series
     - ✅
     - 2025
     - ☑️
     - 
   * - Ryzen Z2
     - Z2
     - Z2
     - Radeon
     - ✅
     - 2025
     - 
     - 
   * - Ryzen AI 300 Series
     - Strix Point
     - STX
     - Radeon 800M Series
     - ✅
     - 2025
     - ☑️
     - 
   * - Ryzen Pro 200 Series
     - Hawk Point
     - HPT
     - Radeon 700M Series
     - ✅
     - 2025
     - ☑️
     - 
   * - Ryzen 200 Series
     - Hawk Point
     - HPT
     - Radeon 700M Series
     - ✅
     - 2025
     - ☑️
     - 
   * - Ryzen PRO 8000 Series
     - Hawk Point
     - HPT
     - Radeon 700M Series
     - ✅
     - 2024
     - ☑️
     - 
   * - Ryzen 8000 Series
     - Hawk Point
     - HPT
     - Radeon 700M Series
     - ✅
     - 2024
     - ☑️
     - 
   * - Ryzen Pro 7000 Series
     - Phoenix
     - PHX
     - Radeon 700M Series
     - ✅
     - 2023
     - ☑️
     - 
   * - Ryzen 7000 Series
     - Phoenix
     - PHX
     - Radeon 700M Series
     - ✅
     - 2023
     - ☑️
     - 

************
LLMs Support
************
Ryzen AI 1.6 supports running LLMs on the hardware configurations in the table below. 

.. list-table:: LLM Support on Ryzen AI Processors
   :header-rows: 1
   :widths: 25 25 25 25 25 25

   * - Processor Series
     - Codename
     - CPU
     - GPU
     - NPU
     - Hybrid (NPU + iGPU)
   * - Ryzen AI 300
     - STX/KRK
     - ✓
     - ✓
     - ✓
     - ✓
   * - Ryzen AI 7000/8000/200
     - PHX/HPT
     - ✓
     - ✓
     - ✗
     - ✗

For more details on running LLMs, refer to the :doc:`llm/overview` page.

*******************
Other Model Support
*******************

The following table lists which types of models are supported on the different hardware platforms.

.. list-table::
   :header-rows: 1

   * - Model Type
     - STX/KRK
     - PHX/HPT
   * - CNN INT8
     - ✓
     - ✓
   * - CNN BF16
     - ✓
     - 
   * - NLP BF16
     - ✓
     - 

***********************
Installation & Examples
***********************
To get started with installing and using Ryzen AI Software, visit the following:

- :doc:`inst`
- :doc:`examples`

*************************
Development Flow Overview
*************************

A typical Ryzen AI flow might look like the following:

1. Begin with a pretrained PyTorch (*.pt) model.
2. Convert the model to ONNX (*.onnx) format. You can follow the PyTorch documentation here: `Export a PyTorch model to ONNX <https://docs.pytorch.org/tutorials/beginner/onnx/export_simple_model_to_onnx_tutorial.html>`_.
3. Optionally, quantize the model with `AMD Quark <https://quark.docs.amd.com/latest/>`_ for a reduced model size.
4. Deploy the model for inference in your application. 
5. Run the :doc:`ai_analyzer` to assess model performance.

.. note::
   You may find that you can skip steps 1-3 and deploy a model right away if you already have an ONNX model that fits on your device.

Quantization
============

Quantization involves converting the AI model’s parameters from floating-point to lower-precision representations, such as 8-bit integer. Quantized models are more power-efficient, utilize less memory, and offer better performance. Ryzen AI Software also supports CNN and Transformer models in floating-point 32 format as input models without quantization. These models are internally converted to bfloat16 and compiled using the bfloat16 compilation flow.


**AMD Quark** is a comprehensive cross-platform deep learning toolkit designed to simplify and enhance the quantization of deep learning models. Supporting both PyTorch and ONNX models, Quark empowers developers to optimize their models for deployment on a wide range of hardware backends, achieving significant performance gains without compromising accuracy.

For more details, refer to the :doc:`model_quantization` page.

Compilation and Deployment
==========================
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
   examples.rst

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Running Models on the NPU

   model_quantization.rst
   modelrun.rst
   app_development.rst

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Running LLMs on the NPU

   llm/overview.rst
   llm/server_interface.rst
   llm/high_level_python.rst
   hybrid_oga.rst
   oga_model_prepare.rst

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Running Models on the GPU

   gpu/ryzenai_gpu.rst


.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Additional Topics

   xrt_smi.rst
   ai_analyzer.rst
   sd_demo.rst
   ryzen_ai_libraries.rst
   Licensing Information <licenses.rst>



..
  ------------
  #####################################
  License
  #####################################

  Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
