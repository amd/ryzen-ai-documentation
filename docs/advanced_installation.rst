.. _advanced_installation.rst:

#####################
Advanced Installation
#####################

This section dives deeper into specific aspects of the installation process, including advanced quantization options and detailed IPU binary configuration.

.. contents:: Table of Contents
   :local:
   :depth: 2

.. _advanced-quantization:

Advanced Quantization
~~~~~~~~~~~~~~~~~~~~~

**Vitis AI PyTorch/TensorFlow 2/TensorFlow Quantization**

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


**Olive Quantization**


Microsoft Olive framework supports quantization with Vitis AI ONNX Quantization. If you're interested in exploring Olive Quantization as an advanced quantization method, you can follow the steps below:

1. Install Olive Quantization by running the following command:

```shell
pip install olive-ai[cpu]
```

2. The current Olive flow is not compatible with the latest pydantic version. To make it compatible, downgrade the pydantic version using the following command:

```shell
pip install pydantic==1.10.9
```

For additional information regarding the Olive installation, refer to the [Microsoft documentation](https://microsoft.github.io/Olive/getstarted/installation.html).


**IPU Binary 5x4.xclbin**
~~~~~~~~~~~~~~~~~~~~~~~~

For more advanced use cases or larger models, IPU binary 5x4.xclbin can be used which uses a larger configuration to provide up to 10 TOPs performance. In the current version of the release, 5x4.xclbin does not support multiple concurrent AI streams, and can only be used by a single application.

Selecting the 5x4.xclbin IPU binary:

```shell
set XLNX_VART_FIRMWARE=C:\path\to\5x4.xclbin
set XLNX_TARGET_NAME="AMD_AIE2_5x4_Overlay"

Note: To select the 5x4.xclbin as the IPU binary, the additional XLNX_TARGET_NAME environment variable is required.

..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
