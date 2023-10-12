###################
Manual Installation
###################

In the main doc:`inst` page, we have shown a one-step installation process that checks the prerequisite and installs ONNX Runtime, Vitis AI execution provider, and Vitis AI ONNX quantizer.

This page shows a manual step-by-step process to install each component. 

Download the installation package and extract. 

.. code-block:

    cd ryzen-ai-sw-0.9\ryzen-ai-sw-0.9

Create Conda Environment
########################

The Ryzen AI Software Platform requires using a conda environment (Anaconda or Miniconda) for the installation process. 

Start a conda prompt. In the conda prompt, create and activate an environment for the rest of the installation process. 

.. code-block:: 

  conda create --name <name> python=3.9
  conda activate <name> 

Install Quantizer
#################

Vitis AI ONNX Quantization is a post-training quantization method that works on models saved in the ONNX format. 

Install Vitis AI ONNX Quantization using the following command:

.. code-block:: shell

   #pip install vai_q_onnx-1.15.0-py2.py3-none-any.whl
   pip install vai_q_onnx-1.15.0+1b31b78-py2.py3-none-any.whl

For other quantization options - Vitis AI PyTorch/TensorFlow 2/TensorFlow Quantization or Olive Quantization, please refer to the :doc:`alternate_quantization_setup` page. 


Install ONNX Runtime
####################

.. code-block::
   
   pip install onnxruntime 


Install Vitis AI Execution Provider
###################################

.. code-block:: 

     cd ryzen-ai-sw-0.9\ryzen-ai-sw-0.9\voe-4.0-win_amd64
     pip install voe-0.1.0-cp39-cp39-win_amd64.whl
     pip install onnxruntime_vitisai-1.15.1-cp39-cp39-win_amd64.whl
     python installer.py
