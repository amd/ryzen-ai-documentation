#######################
Getting Started Example
#######################

This example uses the ResNet-50 model from PyTorch Hub to demonstrate the process of preparing, quantizing, and deploying a model using Ryzen AI.

The following are the steps and the required files to run the example. The files can be downloaded from `here <https://github.com/amd/ryzen-ai-documentation/tree/main/example/resnet50>`_.


.. list-table:: 
   :widths: 20 25 25
   :header-rows: 1

   * - Steps 
     - Files Used
     - Description
   * - Installation
     - ``requirements.txt``
     - Install the necessary package for this example.
   * - Preparation
     - ``prepare_model_data.py``,
       ``resnet_utils.py``
     - Train to prepare a model for the example. The training process adopts the transfer learning technique to train a pre-trained ResNet-50 model with the CIFAR-10 dataset
   * - Quantization 
     - ``resnet_static_config.json``, 
       ``user_script.py``
     - Convert the model to the IPU-deployable model by performing Post-Training Quantization flow using Olive.
   * - Deployment
     - ``predict.py``
     -  Run the Quantized model using ONNX runtime code. We demonstrate running the model on both CPU and IPU. 


|
|

Step 1: Install Packages
~~~~~~~~~~~~~~~~~~~~~~~~

* Ensure that the Ryzen AI SDK is correctly installed. For more details, see :ref:`installation instructions <inst.rst>`.

* This example requires a couple of additional packages. Run the following command to install them:


.. code-block:: 

   python -m pip install -r requirements.txt

|
|

Step 2: Prepare the Model and the Data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this example, we utilize the ResNet-50 model from PyTorch Hub and train it using the CIFAR-10 dataset.

The ``prepare_model_data.py`` script downloads the ResNet-50 model from the PyTorch Hub. The script also downloads the CIFAR10 dataset and uses it to retrain the model using the transfer learning technique. The training process runs over 500 images for each epoch up to five epochs. The training process takes approximately 30 minutes to complete. At the end of the training, we use the trained model for the subsequent steps.

Run the following command to start the training:
 
.. code-block:: 

   python prepare_model_data.py --num_epochs 5

 
A typical output from the training process looks as follows:

.. code-block::

   Downloading: "https://download.pytorch.org/models/resnet50-11ad3fa6.pth" to C:\Users\JohnDoe/.cache\torch\hub\checkpoints\resnet50-11ad3fa6.pth
   100%|██████████████████████████████████████████████████████████████████████████████| 97.8M/97.8M [02:07<00:00, 805kB/s]
   Epoch [1/5], Step [100/500] Loss: 1.1550
   Epoch [1/5], Step [200/500] Loss: 1.0453
   Epoch [1/5], Step [300/500] Loss: 0.6397
   Epoch [1/5], Step [400/500] Loss: 0.6130
   Epoch [1/5], Step [500/500] Loss: 0.6792
   Epoch [2/5], Step [100/500] Loss: 0.5454
   Epoch [2/5], Step [200/500] Loss: 0.5218
   Epoch [2/5], Step [300/500] Loss: 0.7235
   Epoch [2/5], Step [400/500] Loss: 0.5740
   Epoch [2/5], Step [500/500] Loss: 0.9055
   Epoch [3/5], Step [100/500] Loss: 0.5954
   Epoch [3/5], Step [200/500] Loss: 0.4662
   Epoch [3/5], Step [300/500] Loss: 0.3351
   Epoch [3/5], Step [400/500] Loss: 0.4871
   Epoch [3/5], Step [500/500] Loss: 0.4340
   Epoch [4/5], Step [100/500] Loss: 0.4139
   Epoch [4/5], Step [200/500] Loss: 0.4724
   Epoch [4/5], Step [300/500] Loss: 0.4847
   Epoch [4/5], Step [400/500] Loss: 0.4778
   Epoch [4/5], Step [500/500] Loss: 0.3955
   Epoch [5/5], Step [100/500] Loss: 0.5511
   Epoch [5/5], Step [200/500] Loss: 0.4557
   Epoch [5/5], Step [300/500] Loss: 0.6158
   Epoch [5/5], Step [400/500] Loss: 0.3884
   Epoch [5/5], Step [500/500] Loss: 0.4330
   Accuracy of the model on the test images: 75.27 %


After the training process, take note of the following output:
 
* The trained ResNet-50 model on the CIFAR-10 dataset is saved at the following location: ``models\resnet_trained_for_cifar10.pt``.
* The downloaded CIFAR-10 dataset is saved in the current directory at the following location: ``data\cifar-10-batches-py\*``.


|
|

Step 3: Quantize the Model
~~~~~~~~~~~~~~~~~~~~~~~~~~

Quantizing AI models from floating-point to 8-bit integers reduces computational power and the memory footprint required for inference. For model quantization, you have the option to use either Olive or the Vitis AI quantizer. In this example, we will utilize the Olive workflow.

The Olive workflow is configured using the ``resnet_static_config.json`` file. 
 

- First, run Olive in the setup mode 

   .. code-block::

       python -m olive.workflows.run --config resnet_static_config.json --setup

 
- Next, run Olive to convert the model to the ONNX format and quantize it


   .. code-block::

      python -m olive.workflows.run --config resnet_static_config.json 
   
   
   After the run is complete quantized ONNX model ``model.onnx`` is saved inside a cache directory. 

   Example ``model.onnx`` path:  ``./cache/models/1_VitisAIQuantization-0-1586a0b670df52697b3acf9aecd67b24-cpu-cpu/model.onnx``

- Finally, copy the quantized ONNX model in the current working directory for deployment

|
|

Step 4: Deploy the Model  
~~~~~~~~~~~~~~~~~~~~~~~~

The ``predict.py`` script is used to deploy the model. It extracts the first ten images from the CIFAR-10 test dataset and converts them to the .png format. The script then reads all those ten images and classifies them by running the quantized ResNet-50 model on CPU or IPU. 

Deploy the Model on the CPU
===========================

By default ``predict.py`` runs the model on CPU. 

.. code-block::
  
        > python predict.py

Typical output

.. code-block:: 

        Image 0: Actual Label cat, Predicted Label cat
        Image 1: Actual Label ship, Predicted Label ship
        Image 2: Actual Label ship, Predicted Label airplane
        Image 3: Actual Label airplane, Predicted Label airplane
        Image 4: Actual Label frog, Predicted Label frog
        Image 5: Actual Label frog, Predicted Label frog
        Image 6: Actual Label automobile, Predicted Label automobile
        Image 7: Actual Label frog, Predicted Label frog
        Image 8: Actual Label cat, Predicted Label cat
        Image 9: Actual Label automobile, Predicted Label automobile
        
                
Deploy the Model on the Ryzen AI IPU
====================================

To successfully run the model on the IPU, you need to run the following setup steps:

- Ensure that the ``XLNX_VART_FIRMWARE`` environment variable is correctly pointing to the XCLBIN file included in the ONNX Vitis AI Execution Provider package. For more information, see :ref:`installation instructions <set-vart-envar>`.

- Copy the ``vaip_config.json`` runtime configuration file from the Vitis AI Execution Provider package to the current directory. For more information, see :ref:`installation instructions <copy-vaip-config>`. The ``vaip_config.json`` is used by the ``predict.py`` script to configure the Vitis AI Execution Provider.


The following section of the ``predict.py`` script shows how the ONNX Runtime is configured to deploy the model on the Ryzen AI IPU:


.. code-block::

  parser = argparse.ArgumentParser()
  parser.add_argument('--ep', type=str, default ='cpu',choices = ['cpu','ipu'], help='EP backend selection')
  opt = parser.parse_args()
  
  providers = ['CPUExecutionProvider']
  provider_options = [{}]

  if opt.ep == 'ipu':
     providers = ['VitisAIExecutionProvider']
     cache_dir = Path(__file__).parent.resolve()
     provider_options = [{
                'config_file': 'vaip_config.json',
                'cacheDir': str(cache_dir),
                'cacheKey': 'modelcachekey'
                }]

  session = ort.InferenceSession(model.SerializeToString(), providers=providers,
                                 provider_options=provider_options)


Run the ``predict.py`` with the ``--ep ipu`` switch to run the ResNet-50 model on the Ryzen AI IPU:


.. code-block::

    >python predict.py --ep ipu

Typical output

.. code-block:: 

    WARNING: Logging before InitGoogleLogging() is written to STDERR
    I20230610 23:31:05.571316  6032 vitisai_compile_model.cpp:210] Vitis AI EP Load ONNX Model Success
    I20230610 23:31:05.571316  6032 vitisai_compile_model.cpp:211] Graph Input Node Name/Shape (1)
    I20230610 23:31:05.571316  6032 vitisai_compile_model.cpp:215]   input : [-1x3x32x32]
    I20230610 23:31:05.571316  6032 vitisai_compile_model.cpp:221] Graph Output Node Name/Shape (1)
    I20230610 23:31:05.571316  6032 vitisai_compile_model.cpp:225]   output : [-1x10]
    I20230610 23:31:05.579483  6032 vitisai_compile_model.cpp:131] use cache key modelcachekey
    Image 0: Actual Label cat, Predicted Label cat
    Image 1: Actual Label ship, Predicted Label ship
    Image 2: Actual Label ship, Predicted Label airplane
    Image 3: Actual Label airplane, Predicted Label airplane
    Image 4: Actual Label frog, Predicted Label frog
    Image 5: Actual Label frog, Predicted Label frog
    Image 6: Actual Label automobile, Predicted Label automobile
    Image 7: Actual Label frog, Predicted Label frog
    Image 8: Actual Label cat, Predicted Label cat
    Image 9: Actual Label automobile, Predicted Label automobile
 


..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
