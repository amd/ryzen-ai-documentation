#############################################
Model Performance Tuning in Ryzen AI Software
#############################################

This page provides some of the techniques to improve CNN model performance when deploying on the IPU.

1. Enabling Compiler optimization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ryzen-AI software uses ``vaip_config.json`` file to configure the Vitis AI execution provider. 

For CNN-based models, configuration ``opt_level`` can be used to enable advanced compiler optimization can improve model running efficiency on the IPU


.. code-block:: 

    "xcompilerAttrs": {
        ....
        ....
        "opt_level" : {
            "intValue" : 0
        },



The default value of ``opt_level`` is 0, which does not enable any compiler optimization. Set this to 1,2 or 3 to enable increasing levels of compiler optimizations, such as data-movement optimization, control path optimization, and operator fusion. 

- 0 (default): No advanced compiler optimization
- 1: Enable data movement optimization
- 2: Enable data movement and certain control path optimization; 
- 3: Enable data movement, control path, and operator fusion optimization


2. IPU subgraph control (experimental)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ryzen-AI software uses ``vaip_config.json`` file to configure the Vitis AI execution provider. 

For CNN-based models, configuration ``dpu_subgraph_num`` can be used to reduce the number of IPU subgraph. This can help improve performance for complex models where the model can run slow due to a large number of IPU subgraphs. The user can determine the number of subgraph from the ``vaip_ep_report.json`` generated inside the cache directory. This configuration can only be used as an experimental trial.

.. code-block::

    "xcompilerAttrs": {
     .....
     "dpu_subgraph_num" : {
     "intValue" : 32
     },



..
  ------------

  #####################################
  License
  #####################################

  Ryzen AI is licensed under MIT License. Refer to the LICENSE file for the full license text and copyright notice.

    
