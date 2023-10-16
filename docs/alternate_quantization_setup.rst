
#########################
Alternate Quantizer Setup
#########################


Alternate quantizers available in Ryzen-AI software platform as below

1. **PyTorch/TensorFlow 2/TensorFlow Quantization**: If the user requires Quantization Aware Training using the original model training framework, they can use Vitis AI PyTorch/Tensorflow 2/Tensorflow quantizer.
2. **Olive Quantization**: If the user is already familiar with Olive framework and using it for other model transformations, quantization through Olive is also an option. 


.. _install-pt-tf:


Vitis AI PyTorch/TensorFlow 2/TensorFlow Quantization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Vitis AI PyTorch and TensorFlow Quantizer, which is part of the Vitis AI toolchain, require the installation of a Docker container on the host server.

The Vitis AI Docker container can be installed on Ubuntu 20.04, CentOS 7.8, 7.9, 8.1, and RHEL 8.3, 8.4. The developers working on Windows 11 can use WSL for installing Vitis AI Docker.

Multiple versions of the Docker container are available, each tailored to specific frameworks. Follow the Docker download and running instructions as per the following links:

.. list-table:: 
   :widths: 25 25 
   :header-rows: 1

   * - Framework
     - Docker location
   * - PyTorch
     - https://hub.docker.com/r/amdih/ryzen-ai-pytorch
   * - TensorFlow 2
     - https://hub.docker.com/r/amdih/ryzen-ai-tensorflow2
   * - TensorFlow 1
     - https://hub.docker.com/r/amdih/ryzen-ai-tensorflow 


The above Docker containers do not have GPU-accelerated quantization support. If you like to leverage GPU for the quantization process, you can download and build GPU Docker containers. The following TAR file has README that you can follow to build and run GPU dockers.  


https://account.amd.com/en/forms/downloads/ryzen-ai-software-platform-xef.html?filename=ryzen-ai-gpudockerfiles-3.5.0-130.tar.gz

.. _install-olive:

Olive Quantization
~~~~~~~~~~~~~~~~~~


Microsoft Olive framework supports quantization with Vitis AI ONNX Quantization. If you're interested in exploring Olive Quantization as an advanced quantization method, you can follow the steps below:

1. Install Olive Quantization by running the following command:

.. code-block::

    pip install olive-ai[cpu]


2. The current Olive flow is not compatible with the latest pydantic version. To make it compatible, downgrade the pydantic version using the following command:


.. code-block::

    pip install pydantic==1.10.9


For additional information regarding the Olive installation, refer to the [Microsoft documentation](https://microsoft.github.io/Olive/getstarted/installation.html).
