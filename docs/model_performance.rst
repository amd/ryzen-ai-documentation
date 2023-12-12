#############################################
Model Performance Tuning in Ryzen AI Software
#############################################

This page provides some of the techniques to improve CNN model performance when deploying on the IPU.

1. Enabling compiler optimization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ryzen-AI software uses a ``vaip_config.json`` file to configure the Vitis AI Execution Provider. 

For CNN-based models, configuration ``opt_level`` can be used to enable advanced compiler optimization, which can improve model running efficiency on the IPU


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

Ryzen-AI software uses a ``vaip_config.json`` file to configure the Vitis AI Execution Provider. 

For CNN-based models, configuration ``dpu_subgraph_num`` can be used to reduce the number of IPU subgraphs. During the model running stdout shows the number of IPU subgraphs running on IPU as shown below. This configuration can only be used as an experimental trial.

.. code-block::

   ...
   [Vitis AI EP] No. of Subgraphs :   CPU     1    IPU     1 Actually running on IPU     1

If the user sees a large number of IPU subgraphs running on the IPU, they can try to set ``dpu_subgraph_num:intValue`` to a lower value resulting lesser number of IPU subgraphs which can potentially alleviate slow model runtime performance. 

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

    
