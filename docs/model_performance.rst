#################
Model performance
#################

This page provides some of the techniques to improve CNN model performance when deploying on the IPU.

Configuration the Vitis AI EP configuration file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  
Ryzen-AI software uses ``vaip_config.json`` file which configures the Vitis AI execution provider. 

For CNN-based models, a couple of configurations can be used to achieve better performance results. 


1. opt_level
############


.. code-block:: 

    "xcompilerAttrs": {
        ....
        },
        "opt_level" : {
            "intValue" : 0
        },



The default value of opt_level is 0, which does not enable any compiler optimization. Set this to 1,2 or 3 to enable increasing levels of compiler optimizations, such as data-movement optimization, control path optimization, and operator fusion. 

- 0 (default): No advanced compiler optimization
- 1: Enable data movement optimization
- 2: Enable data movement and certain control path optimization; 
- 3: Enable data movement, control path, and operator fusion optimization


2. dpu_subgraph_number
######################


.. code-block::

    "xcompilerAttrs": {
     .....
     "dpu_subgraph_num" : {
     "intValue" : 32
     },




The Ryzen-AI CNN compiler tries to reduce the number of IPU subgraphs so that data movement between CPU and IPU can be minimized, thus helping to improve the runtime performance. For some complex models, it is possible compiler can generate a large number of subgraphs as the default maximum number of subgraph settings is 32. If the user sees a large number of IPU subgraphs (as reported in ``vaip_ep_report.json``), they can set a lower limit to the maximum IPU subgraphs from 32 to a lower value, which can improve the performance. This switch can only be used as an experimental trial.  


..
  ------------

  #####################################
  License
  #####################################

  Ryzen AI is licensed under MIT License. Refer to the LICENSE file for the full license text and copyright notice.

    
