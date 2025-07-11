.. include:: /icons.txt

#######################
Application Development
#######################

This page captures requirements and recommendations for developers looking to create, package and distribute applications targeting NPU-enabled AMD processors.



.. _driver-compatibility:

*************************************
VitisAI EP / NPU Driver Compatibility
*************************************

The VitisAI EP requires a compatible version of the NPU drivers. For each version of the VitisAI EP, compatible drivers are bounded by a minimum version and a maximum release date. NPU drivers are backward compatible with VitisAI EP released up to three years. The maximum driver release date is therefore set to three years after the release date of the corresponding VitisAI EP.

The following table summarizes the driver requirements for the different versions of the VitisAI EP.

.. list-table::
   :header-rows: 1

   * - VitisAI EP version
     - Minimum NPU Driver version
     - Maximum NPU Driver release date
   * - 1.5
     - 32.0.203.280
     - July 1st, 2028
   * - 1.4.1
     - 32.0.203.259
     - May 13th, 2028
   * - 1.4
     - 32.0.203.257
     - March 25th, 2028
   * - 1.3.1
     - 32.0.203.242
     - January 17th, 2028
   * - 1.3
     - 32.0.203.237
     - November 26th, 2027
   * - 1.2
     - 32.0.201.204
     - July 30th, 2027

The application must verify that NPU drivers compatible with the version of the Vitis AI EP in use are installed.

.. _apu-types:

*****************
APU Types
*****************

The Ryzen AI Software supports various types of NPU-enabled APUs, referred to as PHX, HPT, STX, and KRK. To programmatically determine the type of the local APU, you can enumerate the PCI devices and look for an instance with a matching Hardware ID.

.. list-table::
   :header-rows: 1

   * - Vendor
     - Device
     - Revision
     - APU Type
   * - 0x1022
     - 0x1502
     - 0x00
     - PHX or HPT
   * - 0x1022
     - 0x17F0
     - 0x00
     - STX
   * - 0x1022
     - 0x17F0
     - 0x10
     - STX
   * - 0x1022
     - 0x17F0
     - 0x11
     - STX
   * - 0x1022
     - 0x17F0
     - 0x20
     - KRK

The application must verify that it is running on an AMD processor with an NPU, and that the NPU type is supported by the version of the Vitis AI EP in use.



************************************
Application Development Requirements
************************************

ONNX-RT Session
===============

The application should only use the Vitis AI Execution Provider if the following conditions are met:

- The application is running on an AMD processor with an NPU type supported by the version of the Vitis AI EP in use. See :ref:`list <apu-types>`.
- NPU drivers compatible with the version of the Vitis AI EP being used are installed. See :ref:`compatibility table <driver-compatibility>` .

|memo| **NOTE**: Sample C++ code that implements the compatibility checks to be performed before using the Vitis AI EP is available `here <https://github.com/amd/RyzenAI-SW/tree/main/utilities/npu_check>`_


VitisAI EP Provider Options
===========================

For INT8 models, the application should detect the type of APU present (PHX, HPT, STX, or KRK) and set the :option:`xclbin` provider option accordingly. Refer to the section on :ref:`using INT8 models <int8-models>` for more details.

For BF16 models, the application should set the :option:`config_file` provider option to the same file that was used to precompile the BF16 model. Refer to the section on :ref:`using BF16 models <bf16-models>` for more details.


Pre-Compiled Models
===================

To avoid the overhead of recompiling models, it is highly recommended to save the compiled models and use these precompiled versions in the final application. Precompiled models can be loaded instantly and executed immediately on the NPU, significantly improving session creation time and overall end-user experience.

AMD recommends using the ONNXRuntime :ref:`EP Context Cache <ort-ep-context-cache>` feature for saving and reloading compiled models.

.. rubric:: BF16 models

The deployment version of the VitisAI Execution Provider (EP) does not support the on-the-fly compilation of BF16 models. Applications utilizing BF16 models must include pre-compiled versions of these models. The VitisAI EP can then load the pre-compiled models and deploy them efficiently on the NPU.

.. rubric:: INT8 models

Including pre-compiled versions of INT8 models is recommended but not mandatory.

|

.. _app-packaging:

**********************************
Application Packaging Requirements
**********************************

A C++ application built on the Ryzen AI ONNX Runtime must include the following components in its distribution package:

.. rubric:: For INT8 models

- DLLs:

  - %RYZEN_AI_INSTALLATION_PATH%\\deployment\\onnxruntime.dll
  - %RYZEN_AI_INSTALLATION_PATH%\\deployment\\onnxruntime_providers_shared.dll
  - %RYZEN_AI_INSTALLATION_PATH%\\deployment\\onnxruntime_providers_vitisai.dll
  - %RYZEN_AI_INSTALLATION_PATH%\\deployment\\onnxruntime_vitisai_ep.dll
  - %RYZEN_AI_INSTALLATION_PATH%\\deployment\\dyn_dispatch_core.dll
  - %RYZEN_AI_INSTALLATION_PATH%\\deployment\\xaiengine.dll

- NPU Binary files (.xclbin) from the ``%RYZEN_AI_INSTALLATION_PATH%\voe-4.0-win_amd64\xclbins`` folder

- Recommended but not mandatory: pre-compiled models in the form of :ref:`Onnx Runtime EP context models <ort-ep-context-cache>`

.. rubric:: For BF16 models

- DLLs:

  - %RYZEN_AI_INSTALLATION_PATH%\\deployment\\onnxruntime.dll
  - %RYZEN_AI_INSTALLATION_PATH%\\deployment\\onnxruntime_providers_shared.dll
  - %RYZEN_AI_INSTALLATION_PATH%\\deployment\\onnxruntime_providers_vitisai.dll
  - %RYZEN_AI_INSTALLATION_PATH%\\deployment\\onnxruntime_vitisai_ep.dll
  - %RYZEN_AI_INSTALLATION_PATH%\\deployment\\dyn_dispatch_core.dll
  - %RYZEN_AI_INSTALLATION_PATH%\\deployment\\xaiengine.dll
  - %RYZEN_AI_INSTALLATION_PATH%\\deployment\\flexmlrt.dll

- Pre-compiled models in the form of :ref:`Vitis AI EP cache folders <vitisai-ep-cache>`

.. rubric:: For Hybrid LLMs

- DLLs:

  - %RYZEN_AI_INSTALLATION_PATH%\\deployment\\onnxruntime-genai.dll
  - %RYZEN_AI_INSTALLATION_PATH%\\deployment\\onnxruntime.dll
  - %RYZEN_AI_INSTALLATION_PATH%\\deployment\\ryzen_mm.dll
  - %RYZEN_AI_INSTALLATION_PATH%\\deployment\\dyn_dispatch_core.dll
  - %RYZEN_AI_INSTALLATION_PATH%\\deployment\\xaiengine.dll
  - %RYZEN_AI_INSTALLATION_PATH%\\deployment\\onnx_custom_ops.dll
  - %RYZEN_AI_INSTALLATION_PATH%\\deployment\\libutf8_validity.dll
  - %RYZEN_AI_INSTALLATION_PATH%\\deployment\\abseil_dll.dll
  - %RYZEN_AI_INSTALLATION_PATH%\\deployment\\DirectML.dll

.. rubric:: For NPU-only LLMs

- DLLs:

  - %RYZEN_AI_INSTALLATION_PATH%\\deployment\\onnxruntime-genai.dll
  - %RYZEN_AI_INSTALLATION_PATH%\\deployment\\onnxruntime.dll
  - %RYZEN_AI_INSTALLATION_PATH%\\deployment\\ryzen_mm.dll
  - %RYZEN_AI_INSTALLATION_PATH%\\deployment\\dyn_dispatch_core.dll
  - %RYZEN_AI_INSTALLATION_PATH%\\deployment\\xaiengine.dll
  - %RYZEN_AI_INSTALLATION_PATH%\\deployment\\onnxruntime_providers_shared.dll
  - %RYZEN_AI_INSTALLATION_PATH%\\deployment\\onnxruntime_providers_vitisai.dll
  - %RYZEN_AI_INSTALLATION_PATH%\\deployment\\onnxruntime_vitis_ai_custom_ops.dll
  - %RYZEN_AI_INSTALLATION_PATH%\\deployment\\onnxruntime_vitisai_ep.dll

- VAIP LLM configuration file: %RYZEN_AI_INSTALLATION_PATH%\\deployment\\vaip_llm.json


..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
