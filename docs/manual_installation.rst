###################
Manual Installation
###################

In the main :doc:`inst` page, we have shown a one-step installation process that checks the prerequisite and installs Vitis AI ONNX quantizer, ONNX Runtime, and Vitis AI execution provider.

This page shows a manual step-by-step process to install each component. 

Download the installation package and extract. 

https://account.amd.com/en/forms/downloads/ryzen-ai-software-platform-xef.html?filename=ryzen-ai-sw-0.9.zip

.. code-block:

    cd ryzen-ai-sw-0.9\ryzen-ai-sw-0.9

************************
Create Conda Environment
************************

The Ryzen AI Software Platform requires using a conda environment (Anaconda or Miniconda) for the installation process. 

Start a conda prompt. In the conda prompt, create and activate an environment for the rest of the installation process. 

.. code-block:: 

  conda create --name <name> python=3.9
  conda activate <name> 


.. _install-onnx-quantizer:


.. note::

   Please make sure to follow the installation order as shown below

*****************
Install Quantizer
*****************

**Vitis AI ONNX Quantizer** supports a post-training quantization method that works on models saved in the ONNX format. 

Install Vitis AI ONNX Quantization using the following command:

.. code-block:: shell

   cd ryzen-ai-sw-0.9\ryzen-ai-sw-0.9
   pip install vai_q_onnx-1.15.0+a27a6e0-py2.py3-none-any.whl

For other quantization options - Vitis AI PyTorch/TensorFlow 2/TensorFlow Quantization or Olive Quantization, please refer to the :doc:`alternate_quantization_setup` page. 


********************
Install ONNX Runtime
********************

.. code-block::
   
   pip install onnxruntime 


***********************************
Install Vitis AI Execution Provider
***********************************

.. code-block:: 

     cd ryzen-ai-sw-0.9\ryzen-ai-sw-0.9\voe-4.0-win_amd64
     pip install voe-0.1.0-cp39-cp39-win_amd64.whl
     pip install onnxruntime_vitisai-1.15.1-cp39-cp39-win_amd64.whl
     python installer.py
