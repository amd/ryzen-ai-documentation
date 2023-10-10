###################
Model Deployment
###################

.. contents:: Table of Contents


ONNX Runtime with Vitis AI Execution Provider
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After the model is quantized, you can deploy it with ONNX Runtime by utilizing C++ or Python APIs using Vitis AI Execution Provider (VAI EP) for the inference session: 

.. code-block::

  providers = ['VitisAIExecutionProvider']
  session = ort.InferenceSession(model, sess_options = sess_opt,
                                            providers = providers,
                                            provider_options = provider_options)

Provider Options
~~~~~~~~~~~~~~~~

VAI EP supports three provider options:


.. list-table:: 
   :widths: 25 25 25 25
   :header-rows: 1

   * - Provider Options
     - Type
     - Default 
     - Description 
   * - config_file
     - Mandatory
     - None
     - The configuration file ``vaip_config.json`` path. 
       The ``vaip_config.json`` is available inside the setup package.
   * - cacheDir
     - Optional
     - ``C:\temp\{user}\vaip\.cache``
     - The cache directory.
   * - cacheKey
     - Optional 
     - {onnx_model_md5}
     - Used to distinguish between the models. 


Environment Variables
~~~~~~~~~~~~~~~~~~~~~

Additionally, use the following environment variables to control the Ryzen AI ONNX Runtime based deployment.


.. list-table:: 
   :widths: 25 25 25 25
   :header-rows: 1

   * - Environment Variable 
     - Type
     - Default 
     - Description 
   * - XLNX_VART_FIRMWARE
     - Mandatory
     - None
     - The IPU binary ``1x4.xclbin`` file. 
       The ``1x4.xclbin`` is available inside the setup package.
   * - XLNX_ENABLE_CACHE
     - Optional
     - 1
     - If unset, the runtime flow ignores the cache directory and recompiles the model.
     
     
Python API Example
~~~~~~~~~~~~~~~~~~
 
.. code-block::
 
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


C++ API Example
~~~~~~~~~~~~~~~

.. code-block:: 

   // ...
   #include <experimental_onnxruntime_cxx_api.h>
   // include user header files
   // ...

   auto onnx_model_path = "resnet50_pt.onnx"
   Ort::Env env(ORT_LOGGING_LEVEL_WARNING, "resnet50_pt");
   auto session_options = Ort::SessionOptions();

   auto options = std::unorderd_map<std::string,std::string>({});
   options["config_file"] = "/path/to/vaip_config.json";
   options["cacheDir"] = "/path/to/cache/directory";
   options["cacheKey"] = "abcdefg"; // Replace abcdefg with your model name, eg. onnx_model_md5

   // Create an inference session using the Vitis AI execution provider
   session_options.AppendExecutionProvider("VitisAI", options);

   auto session = Ort::Experimental::Session(env, model_name, session_options);

   auto input_shapes = session.GetInputShapes();
   // preprocess input data
   // ...

   // Create input tensors and populate input data
   std::vector<Ort::Value> input_tensors;
   input_tensors.push_back(Ort::Experimental::Value::CreateTensor<float>(
                           input_data.data(), input_data.size(), input_shapes[0]));

   auto output_tensors = session.Run(session.GetInputNames(), input_tensors,
                                      session.GetOutputNames());
   // postprocess output data
   // ...


Model Operators Assignment Report
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Vitis AI EP generates a file named ``vitisai_ep_report.json`` that reports the model operator assignments across CPU and IPU. This report shows device statistics like total number of nodes, number of nodes running on the CPU, and DPU. It also shows a list of all operator types in the model, the list of operators running on the CPU, and on the DPU. The report also shows the node statistics like input to a node, the operation applied, the output from the node, 
and etc.,

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
