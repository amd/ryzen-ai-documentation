##########################
Ryzen AI Software Platform  
##########################

The AMD Ryzen™ AI Software enables developers to take full advantage of the AMD XDNA™-based AI accelerators integrated in AMD Ryzen AI processors. The Ryzen AI Software intelligently optimizes AI tasks and workloads, freeing-up CPU and GPU resources, and ensuring optimal performance at lower power.

**Bring your own model**: the Ryzen AI Software lets developers take machine learning models trained in PyTorch or TensorFlow and deploy them on laptops powered by Ryzen AI processors using the ONNX runtime.

**Use optimized library functions**: the Ryzen AI Library provides ready-made functions optimized for Ryzen AI. Developers can integrate these functions in their applications and harness the power of AI without experience in machine learning required.

|

.. image:: images/landing1.png
   :scale: 75%
   :align: center

|
|

*****************
Table of Contents
*****************

Release Notes
===============

* **Release Notes**: Refer to :doc:`relnotes` page.

Getting Started
===============

* **Installation**: Refer to the :doc:`inst` page. 

* **Runtime Setup**: Refer to the :doc:`runtime_setup` page. 

* **Development Flow Overview**: Refer to the :doc:`devflow` page. 

* **Examples, Demos, and Tutorials**: Refer to the :doc:`examples` page.


Custom Installation
===================

* **Manual Installation Flow**: Refer to the :doc:`manual_installation` page. 

* **Additional Quantizers**: Refer to the :doc:`alternate_quantization_setup` page. 


Using Your Model
================

* **Model Compatibility**: Refer to the :doc:`modelcompat` page. 

* **Model Quantization**: Refer to the :doc:`modelport` page. 

* **Model Running Using ONNX Runtime**: Refer to the the :doc:`modelrun` page. 


Ryzen-AI Libraries
==================

* **Ryzen AI Libraries**: Refer to the :doc:`ryzen_ai_libraries` page

.. toctree::
   :maxdepth: 1
   :caption: Release Notes
   :hidden:

   relnotes.rst


.. toctree::
   :maxdepth: 1
   :caption: Getting Started
   :hidden:

   inst.rst
   runtime_setup.rst
   devflow.rst
   examples.rst

.. toctree::
   :maxdepth: 1
   :caption: Using Your Model
   :hidden:

   modelcompat.rst
   modelport.rst
   modelrun.rst

.. toctree::
   :maxdepth: 1
   :caption: Custom Installation
   :hidden:

   manual_installation.rst
   alternate_quantization_setup.rst  

.. toctree::
   :maxdepth: 1
   :caption: Ryzen AI Libraries
   :hidden:

   ryzen_ai_libraries.rst
 


..
  ------------
  #####################################
  License
  #####################################
  
  Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
