AI Analyzer
===========

AMD AI Analyzer is a powerful tool that supports analysis and visualization of model compilation and inference on the the Ryzen AI NPU. The primary goal of the tool is to help users better understand how the models are processed by the hardware, and to identify performance bottlenecks that may be present during model inference. Using the AI Analyzer, users can effectively visualize graph and operator partitions between the NPU and CPU. 

Features
###########

The AI Analyzer broadly has the following features: 

1. Graph partitions: The tool presents the user with a picture of how the model is paritioned across the CPU and NPU.
2. Operator Fusion: In addition to partitioning, AI Analyzer also presents the user with a picture of how operators have been fused by the compiler. 
4. Inference Profile: The tool provides a breakdown and visualization of inference timing. For this, a Gantt chart of operators is provided. This chart can also be cross-probed to the fused graph.

Installation 
###########

TBD once installation flow is fixed 

Enabling Profiling and Visualization
###########

Profiling and Visualization can be enabled by passing additional provider options to the ONNXRuntime Inference Session. An example is shown below: 

.. code-block::

   provider_options = [{
                'config_file': 'vaip_config.json',
                'cacheDir': str(cache_dir),
                'cacheKey': 'modelcachekey', 
                'ai_analyzer_visualization': True,
                'ai_analyzer_profiling': True,
            }]
  session = ort.InferenceSession(model.SerializeToString(), providers=providers,
                               provider_options=provider_options)

|









..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
