##########################
Ryzen AI Software   
##########################

AMD Ryzen™ AI Software includes the tools and runtime libraries for optimizing and deploying AI inference on AMD Ryzen™ AI powered PCs. Ryzen AI software enables applications to run on the neural processing unit (NPU) built in the AMD XDNA™ architecture, as well as on the integrated GPU. This allows developers to build and deploy models trained in PyTorch or TensorFlow and run them directly on laptops powered by Ryzen AI using ONNX Runtime and the Vitis™ AI Execution Provider (EP).

|

.. image:: images/landing_npu_gpu.png
   :scale: 75%
   :align: center

|
|


.. toctree::
   :maxdepth: 1
   :caption: Release Notes

   relnotes.rst


.. toctree::
   :maxdepth: 1
   :caption: Getting Started on the NPU

   inst.rst
   runtime_setup.rst
   devflow.rst
   examples.rst

.. toctree::
   :maxdepth: 1
   :caption: Using Your CNN on the NPU

   modelcompat.rst
   modelport.rst
   modelrun.rst


.. toctree::
   :maxdepth: 1
   :caption: Running on the GPU

   gpu/ryzenai_gpu.rst
   gpu/gpu_blogs.rst


.. toctree::
   :maxdepth: 1
   :caption: Additional Topics

   Model Zoo <https://huggingface.co/models?other=RyzenAI>
   manual_installation.rst
   alternate_quantization_setup.rst 
   onnx_e2e.rst
   early_access_features.rst


..
  ------------
  #####################################
  License
  #####################################
  
  Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
