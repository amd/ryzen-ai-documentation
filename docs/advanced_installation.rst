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

**Vitis AI ONNX Quantization**

Vitis AI ONNX Quantization is a post-training quantization method that works on models saved in the ONNX format. If you'd like to explore this advanced quantization method, you can follow the installation steps below:

1. Download the installation file from the following link:

   `Vitis AI ONNX Quantization <https://account.amd.com/en/forms/downloads/ryzen-ai-software-platform-xef.html?filename=vai_q_onnx-1.15.0-py2.py3-none-any.whl>`_

2. Install Vitis AI ONNX Quantization using the following command:

.. code-block:: shell

   pip install vai_q_onnx-1.15.0-py2.py3-none-any.whl


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


License
~~~~~~~
Ryzen AI is licensed under the `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_. Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.

