########################
Ryzen AI Developer Guide  
########################

The Ryzen AI SDK enables developers to take machine learning models trained in PyTorch or TensorFlow and run them on laptops powered by `AMD Ryzen™ AI <https://www.amd.com/en/products/ryzen-ai>`__. AMD Ryzen AI is a dedicated AI accelerator integrated on-chip with the CPU cores. The Ryzen AI software intelligently optimizes tasks and workloads, freeing-up CPU and GPU resources and ensuring optimal performance at lower power.

|

.. image:: images/rayzenai.png
   :scale: 75%
   :align: center

|
|

*****************
Table of Contents
*****************

Getting Started
===============

* **Installation**: Refer to :doc:`inst` page. 

* **Release Notes**: Refer to :doc:`relnotes` page.

* **Development Flow Overview**: Refer to :doc:`devflow` page. 

* **Getting Started Example**: Refer to :doc:`getstartex` page to run a resnet50 model example

Using Your Model
================

* **Model Compatibility**: Refer to :doc:`modelcompat` page. 

* **Model Quantization**: Refer to :doc:`modelport` page. 

* **Model Running Using ONNX Runtime**: Refer to the :doc:`modelrun` page. 



.. toctree::
   :maxdepth: 1
   :caption: Getting Started
   :hidden:

   inst.rst
   relnotes.rst
   devflow.rst
   getstartex.rst

.. toctree::
   :maxdepth: 1
   :caption: Using Your Model
   :hidden:

   modelcompat.rst
   modelport.rst
   modelrun.rst

..
  ------------
  #####################################
  License
  #####################################
  
  Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
