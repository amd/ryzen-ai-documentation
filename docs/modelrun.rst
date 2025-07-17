.. include:: /icons.txt

################################
Model Compilation and Deployment
################################


*****************
Introduction
*****************

The Ryzen AI Software supports models saved in the ONNX format and uses ONNX Runtime as the primary mechanism to load, compile and run models. 

|memo| **NOTE**: Models with ONNX opset 17 are recommended. If your model uses a different opset version, consider converting it using the `ONNX Version Converter <https://github.com/onnx/onnx/blob/main/docs/VersionConverter.md>`_

For a complete list of supported operators, consult this page: :doc:`Supported Operators <ops_support>`.

Loading Models
==============

Models are loaded by creating an ONNX Runtime ``InferenceSession`` using the Vitis AI Execution Provider (VAI EP):

.. code-block:: python

    import onnxruntime

    session_options = onnxruntime.SessionOptions()
    vai_ep_options  = {}                          # Vitis AI EP options go here

    session = onnxruntime.InferenceSession(
        path_or_bytes = model,                    # Path to the ONNX model
        sess_options = session_options,           # Standard ORT options
        providers = ['VitisAIExecutionProvider'], # Use the Vitis AI Execution Provider
        provider_options = [vai_ep_options]       # Pass options to the Vitis AI Execution Provider
    )


The ``provider_options`` parameter enables the configuration of the Vitis AI Execution Provider (EP). For a comprehensive list of supported provider options, refer to the :ref:`Vitis AI EP Options Reference Guide <ep-options-ref-guide>` below.

When a model is first loaded into an ONNX Runtime (ORT) inference session, it is compiled into the format required by the NPU. The resulting compiled output can be saved as an ORT EP context file or stored in the Vitis AI EP cache directory.

If a compiled version of the ONNX model is already available — either as an EP context file or within the Vitis AI EP cache — the model will not be recompiled. Instead, the precompiled version will be loaded automatically. This greatly reduces session creation time and improves overall efficiency. For more details, refer to the section on :ref:`Managing Compiled Models <precompiled-models>`.


Deploying Models
================

Once the ONNX Runtime inference session is initialized and the model is compiled, the model is deployed using the ONNX Runtime ``run()`` API:

.. code-block:: python

    input_data = {}
    for input in session.get_inputs():
        input_data[input.name] = …  # Initialize input tensors

    outputs = session.run(None, input_data) # Run the model


The ONNX graph is automatically partitioned into multiple subgraphs by the Vitis AI Execution Provider (EP). During deployment, the subgraph(s) containing operators supported by the NPU are executed on the NPU. The remaining subgraph(s) are executed on the CPU. This graph partitioning and deployment technique across CPU and NPU is fully automated by the VAI EP and is totally transparent to the end-user.


.. _ep-options-ref-guide:

***********************************
Vitis AI EP Options Reference Guide
***********************************

VitisAI EP Provider Options
===========================

The ``provider_options`` parameter of the ORT ``InferenceSession`` allows passing options to configure the Vitis AI EP. The following options are supported.


- .. option:: config_file 

Optional. Configuration file to pass additional compilation options for BF16 models. For more details, refer to the section about :ref:`Config File Options <configuration-file>`.

Type: String

Default: N/A


- .. option:: xclbin

Required for INT8 models. NPU binary file to specify NPU configuration to be used for INT8 models. For more details, refer to the section about :ref:`Using INT8 Models <int8-models>`.

Type: String

Default: N/A.


- .. option:: encryption_key 

Optional. 256-bit key used for encrypting the EP context model. At runtime, you must use the same key to decrypt the model when loading it. For more details, refer to the section about the :ref:`EP Context Cache <ort-ep-context-cache>` feature.

Type: String of 64 hexadecimal values representing the 256-bit encryption key.

Default: None, the model is not encrypted.


- .. option:: opt_level 

Optional. Applies to INT8 models only. Controls the compiler optimization effort.

Supported Values: 0, 1, 2, 3, 65536 (maximum effort, experimental)

Default: 0


- .. option:: log_level

Optional. Controls what level of messages are reported by the VitisAI EP.

Supported Values: "info", "warning", "warning", "error", "fatal"

Default: "info"


- .. option:: cache_dir 

Optional. The path and name of the VitisAI cache directory. For INT8 models, for this option to take affect, the :option:`enable_cache_file_io_in_mem` must be set to 0. For more details, refer to the section about :ref:`VitisAI cache <vitisai-ep-cache>`.

Type: String

Default: C:\\temp\\%USERNAME%\\vaip\\.cache


- .. option:: cache_key 

Optional. The subfolder in the VitisAI cache directory where the compiled model is stored. For INT8 models, for this option to take affect, the :option:`enable_cache_file_io_in_mem` must be set to 0. For more details, refer to the section about :ref:`VitisAI cache <vitisai-ep-cache>`.

Type: String

Default: MD5 hash of the input model.


- .. option:: enable_cache_file_io_in_mem

Optional. Applies to INT8 models only. By default, the VitisAI EP keeps the compiled model in memory. To enable saving the compiled model to disk in the :option:`cache_dir` folder, :option:`enable_cache_file_io_in_mem` must be set to 0.

Supported Values: 0, 1

Default: 1


- .. option:: ai_analyzer_visualization 

Optional. Enables generation of compile-time analysis data.

Type: Boolean

Default: False


- .. option:: ai_analyzer_profiling 

Optional. Enables generation of inference-time analysis data.

Type: Boolean

Default: False


.. _configuration-file:

Config File Options
===================

When compiling BF16 models, a JSON configuration file can be provided to the VitisAI EP using the :option:`config_file` provider option. This configuration file is used to specify additional options to the compiler. 

The default the configuration file for compiling BF16 models contains the following:

.. code-block:: json

   {
    "passes": [
        {
            "name": "init",
            "plugin": "vaip-pass_init"
        },
        {
            "name": "vaiml_partition",
            "plugin": "vaip-pass_vaiml_partition",
            "vaiml_config": {
                "optimize_level": 1,
                "preferred_data_storage": "auto"
            }
        }
    ]
   }


The ``vaiml_config`` section of the configuration file contains the user options. The supported user options are described below.


- .. option:: optimize_level

Controls the compiler optimization level.

Supported values: 1 (default), 2, 3



- .. option:: preferred_data_storage

Controls whether intermediate data is stored in vectorized or unvectorized format. Models dominated by convolutions (e.g., CNNs) perform better with vectorized data. Models dominated by GEMMs (e.g., Transformers) perform better with unvectorized data. By default ("auto") the compiler tries to select the best layout.

Supported values: "auto" (default), "vectorized", "unvectorized"



.. _bf16-models:

**************************
Using BF16 models
**************************

When compiling BF16 models, a configuration file must be provided to the VitisAI EP. This file is specified using the :option:`config_file` provider option. For more details, refer to :ref:`Config File Options <configuration-file>` section.

Sample Python Code
==================

Python example loading a configuration file called vai_ep_config.json:

.. code-block:: python

    import onnxruntime

    vai_ep_options = {
        'config_file': 'vai_ep_config.json'
    }

    session = onnxruntime.InferenceSession(
        "resnet50_bf16.onnx",
        providers=['VitisAIExecutionProvider'],
        provider_options=[vai_ep_options]
    )


Sample C++ Code
===============

C++ example loading a configuration file called vai_ep_config.json:

.. code-block:: cpp

    #include <onnxruntime_cxx_api.h>

    auto onnx_model = "resnet50_bf16.onnx"
    Ort::Env env(ORT_LOGGING_LEVEL_WARNING, "resnet50_bf16");
    auto session_options = Ort::SessionOptions();
    auto vai_ep_options = std::unorderd_map<std::string,std::string>({});
    vai_ep_options["config_file"] = "vai_ep_config.json";
    session_options.AppendExecutionProvider_VitisAI(vai_ep_options);
    auto session = Ort::Session(
        env, 
        std::basic_string<ORTCHAR_T>(onnx_model.begin(), onnx_model.end()).c_str(), 
        session_options);


.. _int8-models:

**************************
Using INT8 models
**************************

When compiling INT8 models, the NPU configuration must be specified through the :option:`xclbin` provider option. This option is not required for BF16 models. 

Setting the NPU configuration involves specifying one of ``.xclbin`` binary files located in the Ryzen AI Software installation tree.

It is recommended to copy the required xclbin files from the Ryzen AI installation tree into the project folder as the xclbin files used to compile the model must be included in the final version of the application. 

Depending on the target processor type, the following ``.xclbin`` files should be used:

**For STX/KRK APUs**:

- ``%RYZEN_AI_INSTALLATION_PATH%\voe-4.0-win_amd64\xclbins\strix\AMD_AIE2P_4x4_Overlay.xclbin``

**For PHX/HPT APUs**:

- ``%RYZEN_AI_INSTALLATION_PATH%\voe-4.0-win_amd64\xclbins\phoenix\4x4.xclbin``


|memo| **NOTE**: Starting in Ryzen AI 1.5, the legacy "1x4" and "Nx4" xclbin files are no longer supported and should not be used.


Sample Python Code
==================

Python example selecting the ``AMD_AIE2P_4x4_Overlay.xclbin`` NPU configuration for STX/KRK located in the Ryzen AI installation folder:

.. code-block:: python

    import os
    import onnxruntime

    vai_ep_options = {
        'xclbin': os.path.join(os.environ['RYZEN_AI_INSTALLATION_PATH'], 'voe-4.0-win_amd64', 'xclbins', 'strix', 'AMD_AIE2P_4x4_Overlay.xclbin')
    }

    session = onnxruntime.InferenceSession(
        "resnet50_int8.onnx",
        providers=['VitisAIExecutionProvider'],
        provider_options=[vai_ep_options]
    )


Sample C++ Code
===============

C++ example selecting the ``AMD_AIE2P_4x4_Overlay.xclbin`` NPU configuration for STX/KRK located in a custom folder:

.. code-block:: cpp

    #include <onnxruntime_cxx_api.h>

    auto onnx_model = "resnet50_int8.onnx"
    Ort::Env env(ORT_LOGGING_LEVEL_WARNING, "resnet50_int8");
    auto session_options = Ort::SessionOptions();
    auto vai_ep_options = std::unorderd_map<std::string,std::string>({});
    vai_ep_options["xclbin"] = "/path/to/xclbins/strix/AMD_AIE2P_4x4_Overlay.xclbin";
    session_options.AppendExecutionProvider_VitisAI(vai_ep_options);
    auto session = Ort::Session(
        env, 
        std::basic_string<ORTCHAR_T>(onnx_model.begin(), onnx_model.end()).c_str(), 
        session_options);

|


.. _precompiled-models:

************************************
Managing Compiled Models
************************************

To avoid the overhead of recompiling models, it is very advantageous to save the compiled models and use these pre-compiled versions in the final application. Pre-compiled models can be loaded instantaneously and immediately executed on the NPU. This greatly improves the session creation time and overall end-user experience.

The RyzenAI Software supports two mechanisms for saving and reloading compiled models:

- VitisAI EP Cache
- ONNX Runtime EP Context Cache

|bulb| **TIP**: The VitisAI EP Cache mechanism is most convenient to quickly iterate during the development cycle. The OnnxRuntime EP Context Cache mechanism is recommended for the final version of the application.  


.. _vitisai-ep-cache:

VitisAI EP Cache
================

The VitisAI EP includes a built-in caching mechanism. When a model is compiled for the first time, it is automatically saved in the VitisAI EP cache directory. Any subsequent creation of an ONNX Runtime session using the same model will load the precompiled model from the cache directory, thereby reducing session creation time.

The VitisAI EP Cache mechanism can be used to quickly iterate during the development cycle, but it is not recommended for the final version of the application.

Cache directories generated by the Vitis AI Execution Provider should not be reused across different versions of the Vitis AI EP or across different version of the NPU drivers.

If using the VitisAI EP Cache the application should check the version of the Vitis AI EP and of the NPU drivers. If the application detects a version change, it should delete the cache, or create a new cache directory with a different name.

The location of the VitisAI EP cache is specified with the :option:`cache_dir` and :option:`cache_key` provider options. For INT8 models, the :option:`enable_cache_file_io_in_mem` must be set to 0 otherwise the output of the compiler is kept in memory and is not saved to disk.


Python example:

.. code-block:: python

    import onnxruntime
    from pathlib import Path

    vai_ep_options = {
        'cache_dir': str(Path(__file__).parent.resolve()),
        'cache_key': 'compiled_resnet50_int8',
        'enable_cache_file_io_in_mem': 0
    }

    session = onnxruntime.InferenceSession(
        "resnet50_int8.onnx",
        providers=['VitisAIExecutionProvider'],
        provider_options=[vai_ep_options]
    )


In the example above, the cache directory is set to the absolute path of the folder containing the script being executed. Once the session is created, the compiled model is saved inside a subdirectory named ``compiled_resnet50_int8`` within the specified cache folder.


.. _ort-ep-context-cache:

ONNX Runtime EP Context Cache
=============================

The Vitis AI EP supports the ONNX Runtime EP context cache feature. This features allows dumping and reloading a snapshot of the EP context before deployment. 

The user can enable dumping of the EP context by setting the ``ep.context_enable`` session option to 1.

The following options can be used for additional control:

- ``ep.context_file_path`` – Specifies the output path for the dumped context model.
- ``ep.context_embed_mode`` – Embeds the EP context into the ONNX model when set to 1.

For further details, refer to the official ONNX Runtime documentation: https://onnxruntime.ai/docs/execution-providers/EP-Context-Design.html


EP Context Encryption
---------------------

By default, the generated context model is unencrypted and can be used directly during inference. If needed, the context model can be encrypted using one of the methods described below. 

User-managed encryption
~~~~~~~~~~~~~~~~~~~~~~~
After the context model is generated, the developer can encrypt the generated file using a method of choice. At runtime, the encrypted file can be loaded by the application, decrypted in memory and passed as a serialized string to the inference session. 

This method gives complete control to the developer over the encryption process.

EP-managed encryption
~~~~~~~~~~~~~~~~~~~~~~~
The VitisAI EP can optionally encrypt the EP context model using AES256. This is enabled by passing an encryption key using the :option:`encryption_key` VAI EP provider options. The key is a 256-bit value represented as a 64-digit string. At runtime, the same encryption key must be provided to decrypt and load the context model. 

With this method, encryption and decryption is seamlessly managed by the VitisAI EP.


Python example:

.. code-block:: python

    import onnxruntime

    vai_ep_options = {
        'xclbin': r'/path/to/xclbins/strix/AMD_AIE2P_4x4_Overlay.xclbin'),
        'encryptionKey': '89703f950ed9f738d956f6769d7e45a385d3c988ca753838b5afbc569ebf35b2'
    }

    # Compilation session
    session_options = ort.SessionOptions()
    session_options.add_session_config_entry('ep.context_enable', '1')
    session_options.add_session_config_entry('ep.context_file_path', 'context_model.onnx')
    session_options.add_session_config_entry('ep.context_embed_mode', '1')
    session = ort.InferenceSession(
        path_or_bytes='resnet50_int8.onnx',  # Load the ONNX model
        sess_options=session_options,
        providers=['VitisAIExecutionProvider'],
        provider_options=[vai_ep_options]
    )

    # Inference session
    session_options = ort.SessionOptions()
    session = ort.InferenceSession(
        path_or_bytes='context_model.onnx', # Load the EP context model
        sess_options=session_options,
        providers=['VitisAIExecutionProvider'],
        provider_options=[vai_ep_options]
    )


C++ example:

.. code-block:: cpp

    Ort::Env env(ORT_LOGGING_LEVEL_WARNING, "ort");

    // VAI EP Provider options
    auto vai_ep_options = std::unorderd_map<std::string,std::string>({});
    vai_ep_options["xclbin"] = "/path/to/xclbins/strix/AMD_AIE2P_4x4_Overlay.xclbin";
    vai_ep_options["encryption_key"] = "89703f950ed9f738d956f6769d7e45a385d3c988ca753838b5afbc569ebf35b2";

    // Session options
    auto session_options = Ort::SessionOptions();
    session_options.AppendExecutionProvider_VitisAI(vai_ep_options);

    // Inference session
    auto onnx_model = "context_model.onnx"; // The EP context model
    auto session = Ort::Session(
        env, 
        std::basic_string<ORTCHAR_T>(onnx_model.begin(), onnx_model.end()).c_str(), 
        session_options);


|memo| **NOTE**: It is possible to precompile the EP context model using Python and to deploy it using a C++ program.


|

.. _op-assignment-report:

**************************
Operator Assignment Report
**************************

The compiler can optionally generate a report on operator assignments across CPU and NPU. To generate this report:

- The :option:`enable_cache_file_io_in_mem` provider option must be set to 0
- The XLNX_ONNX_EP_REPORT_FILE environment variable must be used to specify the name of the generated report. For instance:

.. code-block::

    set XLNX_ONNX_EP_REPORT_FILE=vitisai_ep_report.json

When these conditions are satisfied, the report file is automatically generated in the cache directory. This report includes information such as the total number of nodes, the list of operator types in the model, and which nodes and operators run on the NPU or on the CPU. Additionally, the report includes node statistics, such as input to a node, the applied operation, and output from the node.

When these conditions are satisified, the report file is automatically generated in the cache directory. This report includes information such as the total number of nodes, the list of operator types in the model, and which nodes and operators runs on the NPU or on the CPU. Additionally, the report includes node statistics, such as input to a node, the applied operation, and output from the node.

.. code-block::

  {
   "deviceStat": [
   {
    "name": "all",
    "nodeNum": 400,
    "supportedOpType": [
     "::Add",
     "::Conv",
     ...
    ]
   },
   {
    "name": "CPU",
    "nodeNum": 2,
    "supportedOpType": [
     "::DequantizeLinear",
     "::QuantizeLinear"
    ]
   },
   {
    "name": "NPU",
    "nodeNum": 398,
    "supportedOpType": [
     "::Add",
     "::Conv",
     ...
    ]
    ...


To disable generation of the report, unset the XLNX_ONNX_EP_REPORT_FILE environment variable:

.. code-block::

    set XLNX_ONNX_EP_REPORT_FILE=


..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
