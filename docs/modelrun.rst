.. include:: icons.txt

################################
Model Compilation and Deployment
################################

The Ryzen AI Software supports deploying quantized model saved in the ONNX format.

Currently, the NPU supports a subset of the ONNX operators. At runtime, the ONNX graph is automatically partitioned into multiple subgraphs by the Vitis AI ONNX Execution Provider (VAI EP). The subgraph(s) containing operators supported by the NPU are executed on the NPU. The remaining subgraph(s) are executed on the CPU. This graph partitioning and deployment technique across CPU and NPU is fully automated by the VAI EP and is totally transparent to the end-user.

|memo| **NOTE**: Models with ONNX opset 17 are recommended. If your model uses a different opset version, consider converting it using the `ONNX Version Converter <https://github.com/onnx/onnx/blob/main/docs/VersionConverter.md>`_

*****************
Model Compilation
*****************

Quantized models are compiled targetting NPU when an ONNX inference session is created by leveraring the Vitis AI Execution Provider (VAI EP). 

.. code-block:: python

  providers = ['VitisAIExecutionProvider']
  session = ort.InferenceSession(model, sess_options = sess_opt,
                                            providers = providers,
                                            provider_options = provider_options)

Depending on the model, model compilation can take sometime. However, after compilation compiled model is saved inside the cache directory. Hence any susequent run of the onnxruntime script simply picks the compiled model from the cache directory. 

Vitis AI Execution Provider Options
===================================

The Vitis AI Execution Provider supports the following options:

- config_file: Configuration file to guide model compilation and runtime. 

  - For INT8 Model the configuration file is not required. 
  - For BF16 Models configuration files are provided in the bf16 examples

- cache_dir: The top level cache directory of the compiled models. If not provided cache_dir is ``C:\temp\{user}\vaip\.cache``
- cache_key: Compiled model directory generated inside the cache directory. Use string to specify the desired name of the compiler model directory. For example,  ``'cacheKey': 'resnet50_cache'``

.. note::

   unset XLNX_ENABLE_CACHE environment variable in the command prompt results ignoring the cache and recompile the model. 

- encryptionKey (optional): Encryption/Decryption key for the models generated. 

- xclbin : Target NPU configuration, only required for INT8 compilation. For INT8 compilation Ryzen AI supports two NPU configuration, standard and benchmark. 

  - Setting standard configuration for INT8 models

    - For STX/KRK APUs:

      .. code-block::

           provider_options = [{
               'xclbin' : 'C:\Program Files\RyzenAI\1.4.0\voe-4.0-win_amd64\xclbins\strix\C:\Program Files\RyzenAI\1.4.0\voe-4.0-win_amd64\xclbins\strix\AMD_AIE2P_Nx4_Overlay.xclbin'                    
       }]

    - For PHX/HPT APUs:

      .. code-block::

          provider_options = [{
              'xclbin' : 'C:\Program Files\RyzenAI\1.4.0\voe-4.0-win_amd64\xclbins\strix\C:\Program Files\RyzenAI\1.4.0\voe-4.0-win_amd64\xclbins\phoenix/1x4.xclbin'                    
        }]


  - Setting benchmark configuration for INT8 models

    - For STX/KRK APUs:

      .. code-block::

           provider_options = [{
               'xclbin' : 'C:\Program Files\RyzenAI\1.4.0\voe-4.0-win_amd64\xclbins\strix\C:\Program Files\RyzenAI\1.4.0\voe-4.0-win_amd64\xclbins\strix/AMD_AIE2P_4x4_Overlay.xclbin'                    
       }]

    - For PHX/HPT APUs:

      .. code-block::

          provider_options = [{
              'xclbin' : 'C:\Program Files\RyzenAI\1.4.0\voe-4.0-win_amd64\xclbins\strix\C:\Program Files\RyzenAI\1.4.0\voe-4.0-win_amd64\xclbins\phoenix/4x4.xclbin'                    
        }]


     
|

******************
Python API Example
******************
 
.. code-block:: python
 
    import onnxruntime

    # Add user imports
    # ...
 
    # Load inputs and perform preprocessing
    # ...

    # Create an inference session using the Vitis AI execution provider
    session = onnxruntime.InferenceSession(
                  '[model_file].onnx',
                   providers=["VitisAIExecutionProvider"],
                   provider_options=[{"config_file":"/path/to/vaip_config.json"}])

    input_shape = session.get_inputs()[0].shape
    input_name = session.get_inputs()[0].name

    # Load inputs and do preprocessing by input_shape
    input_data = [...]
    result = session.run([], {input_name: input_data})  

|

***************
C++ API Example
***************

.. code-block:: cpp

    #include <onnxruntime_cxx_api.h>
    // include user header files
    // ...
    std::string xclbin_path = "path/to/xclbin";
    std::string model_path  = "path/to/model.onnx";
    std::string config_path = "path/to/config.json";
    auto model_name = strconverter.from_bytes(model_path);
    
    _putenv_s("XLNX_VART_FIRMWARE", xclbin_path.c_str());
    
    Ort::Env env(ORT_LOGGING_LEVEL_WARNING, "quicktest");
    
    // create inference session
    auto session_options = Ort::SessionOptions();
    auto options = std::unordered_map<std::string, std::string>{ 
        {"config_file", config_path},          // Required
        {"cacheDir",    "path/to/cacheDir"},   // Optional
        {"cacheKey",    "cacheName"}           // Optional
    };
    session_options.AppendExecutionProvider_VitisAI(options);
    auto session = Ort::Session(env, model_path.data(), session_options);

    // preprocess input data
    // ...


    // get input/output names from model
    size_t                   input_count;
    size_t                   output_count;
    std::vector<const char*> input_names; 
    std::vector<const char*> output_names;
    ...
    
    // initialize input tensors
    std::vector<Ort::Value>  input_tensors;
    ... 
    
    // run inference
    auto output_tensors = session.Run(
            Ort::RunOptions(), 
            input_names.data(), input_tensors.data(), input_count, 
            output_names.data(), output_count);
 
    // postprocess output data
    // ...

|

*********************
Simultaneous Sessions
*********************

Up to eight simultaneous inference sessions can be run on the NPU. The runtime automatically schedules each inference session on available slots to maximize performance of the application. 

The performance of individual inference sessions is impacted by multiple factors, including the APU type, the NPU configuration used, the number of other inference sessions running on the NPU, and the applications running the inference sessions.

|

****************
Model Encryption
****************

To protect developers’ intellectual property, encryption is supported as a session option.
With this enabled, all the compiled models generated are encrypted using AES256.
To enable encryption, you need to pass the encryption key through the VAI EP options as follows:

In Python:

.. code-block:: python
 
    session = onnxruntime.InferenceSession(
        '[model_file].onnx',
        providers=["VitisAIExecutionProvider"],
        provider_options=[{
            "config_file":"/path/to/vaip_config.json",
            "encryptionKey": "89703f950ed9f738d956f6769d7e45a385d3c988ca753838b5afbc569ebf35b2"
    }])

In C++:

.. code-block:: cpp

    auto onnx_model_path = "resnet50_pt.onnx"
    Ort::Env env(ORT_LOGGING_LEVEL_WARNING, "resnet50_pt");
    auto session_options = Ort::SessionOptions();
    auto options = std::unorderd_map<std::string,std::string>({});
    options["config_file"] = "/path/to/vaip_config.json";
    options["encryptionKey"] = "89703f950ed9f738d956f6769d7e45a385d3c988ca753838b5afbc569ebf35b2";

    session_options.AppendExecutionProvider("VitisAI", options);
    auto session = Ort::Experimental::Session(env, model_name, session_options);

The key is a 256-bit value represented as a 64-digit string. The model generated in the cache directory cannot be opened with Netron currently. Additionally, there is a side effect: dumping is disabled to prevent the leakage of sensitive information about the model.

|

**************************
Operator Assignment Report
**************************


Vitis AI EP generates a file named ``vitisai_ep_report.json`` that provides a report on model operator assignments across CPU and NPU. This file is automatically generated in the cache directory, which by default is ``C:\temp\{user}\vaip\.cache\<model_cache_key>`` if no explicit cache location is specified in the code. This report includes information such as the total number of nodes, the list of operator types in the model, and which nodes and operators runs on the NPU or on the CPU. (NOTE: Nodes and operators running on the NPU are reported under the DPU name). Additionally, the report includes node statistics, such as input to a node, the applied operation, and output from the node.


.. code-block:: 

  {
    "deviceStat": [
    {
      "name": "all",
      "nodeNum": 402,
      "supportedOpType": [
      "::Add",
      ...
      ]
    },
    {
      "name": "CPU",
      "nodeNum": 2,
      "supportedOpType": [
      "::DequantizeLinear",
      ...
      ]
    },
    {
      "name": "DPU",
      "nodeNum": 400,
      "supportedOpType": [
      "::Add",
      ...
      ]
    }
    ],
    ...

..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
