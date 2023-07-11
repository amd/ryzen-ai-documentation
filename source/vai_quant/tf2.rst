#######################
Tensorflow Quantization
#######################

.. note:: 

    All Tensorflow related documentation is applicable to Tensorflow 2 version. 


Enabling Quantization
~~~~~~~~~~~~~~~~~~~~~

To enable Vitis AI Tensorflow Quantization, acvitate the conda environment inside the Vitis AI Tensorflow 2 docker container:

.. code-block::

     conda activate vitis-ai-tensorflow2
     

Post-Training Quantization
~~~~~~~~~~~~~~~~~~~~~~~~~~

Post-Training Quantization requires the following files:

1. Float model : Floating-point TensorFlow models, either in h5 format or a saved model format.
2. Calibration dataset: A subset of the training dataset containing 100 to 1000 images.
 
 
A complete example of Post-Training Quantization is available at `Vitis AI GitHub <https://github.com/Xilinx/Vitis-AI/blob/v3.0/src/vai_quantizer/vai_q_tensorflow2.x/tensorflow_model_optimization/python/examples/quantization/keras/vitis/mnist_cnn_ptq.py>`__
     
Vitis AI Quantization APIs
%%%%%%%%%%%%%%%%%%%%%%%%%%     

Vitis AI provides the ``vitis_activation`` module into Tensorflow library for quantization. The following code shows the usage:

.. code-block::

   model = tf.keras.models.load_model(‘float_model.h5’)
   from tensorflow_model_optimization.quantization.keras import vitis_quantize
   quantizer = vitis_quantize.VitisQuantizer(model)
   quantized_model = quantizer.quantize_model(calib_dataset=calib_dataset,calib_steps=100,calib_batch_size=10, **kwargs)
   

- calib_dataset: Used as a representative calibration dataset for calibration. 
- calib_steps: Total number of steps for calibration. 
- calib_batch_size: Number of samples per batch for calibration. 
- input_shape: Input shape for each input layer. 
- kwargs: dict of the user-defined configurations of quantize strategy. 

Exporting the Model for Deployment
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

After the quantization, the quantized model can be saved into ONNX to deploy with ONNX runtime Vitis AI execution provider: 

.. code-block::

   quantized_model = quantizer.quantize_model(calib_dataset=calib_dataset, 
                                              output_format='onnx', 
                                              onnx_opset_version=11, 
                                              output_dir='./quantize_results', 
                                              **kwargs)

Fast Finetuning
%%%%%%%%%%%%%%%

After post-training quantization, usually there is a small accuracy loss. If the accuracy loss is large, a fast-finetuning approach, which is based on the `AdaQuant Algorithm <https://arxiv.org/abs/2006.10518>`__, can be tried instead of quantization aware training. The fast finetuning uses a small unlabeled data to calibrate the activations and finetuning the weights. 

.. code-block::

   quantized_model = quantizer.quantize_model(calib_dataset=calib_dataset, calib_steps=None, calib_batch_size=None, 
                                              include_fast_ft=True, fast_ft_epochs=10)
                                              
Fast finetuning related parameters

- include_fast_ft indicates whether to do fast finetuning or not.
- fast_ft_epochs indicates the number of finetuning epochs for each layer.


Quantization Aware Training
~~~~~~~~~~~~~~~~~~~~~~~~~~~


An example of Quantization Aware Training is available at `Vitis Github <https://github.com/Xilinx/Vitis-AI/blob/v3.0/src/vai_quantizer/vai_q_tensorflow2.x/tensorflow_model_optimization/python/examples/quantization/keras/vitis/mnist_cnn_qat.py>`__ 


General steps are:

1. Prepare floating point model, training dataset and training script.
2. Modify the training by using ``VitisQuantizer.get_qat_model`` to convert the model to a quantized model and then proceed to training/finetuning with it.

.. code-block::

   model = tf.keras.models.load_model(‘float_model.h5’)
   # Call Vai_q_tensorflow2 api to create the quantize training model
   from tensorflow_model_optimization.quantization.keras import vitis_quantize
   quantizer = vitis_quantize.VitisQuantizer(model)
   qat_model = quantizer.get_qat_model(init_quant=True, 
                                       calib_dataset=calib_dataset)
                                       
   # Then run the training process with this qat_model to get the quantize finetuned model.
   # Compile the model
   qat_model.compile(optimizer= RMSprop(learning_rate=lr_schedule),
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(),
                  metrics=keras.metrics.SparseTopKCategoricalAccuracy())
   
   # Start the training/finetunin
   qat_model.fit(train_dataset)

3. Call ``model.save()`` to save the trained model or use callbacks in ``model.fit()`` to save the model periodically.

.. code-block::
 
    # save model manually
    qat_model.save(‘trained_model.h5’)
    
    # save the model periodically during fit using callbacks
    qat_model.fit(train_dataset,
                  callbacks = [
                         keras.callbacks.ModelCheckpoint(
                         filepath=’./quantize_train/’
                         save_best_only=True,
                         monitor="sparse_categorical_accuracy",
                         verbose=1,
                  )])
                  
5. Convert the model to deployable state by ``get_deploy_model`` API.

.. code-block::

   quantized_model = vitis_quantizer.get_deploy_model(qat_model)
   quantized_model = quantizer.quantize_model(calib_dataset=calib_dataset, 
                                              output_format='onnx', 
                                              onnx_opset_version=11, 
                                              output_dir='./quantize_results',**kwargs)

..
  ------------

  #####################################
  Please Read: Important Legal Notices
  #####################################

  The information presented in this document is for informational purposes only and may contain technical inaccuracies, omissions, and typographical errors. The information contained herein is subject to change and may be rendered inaccurate for many reasons, including but not limited to product and roadmap changes, component and motherboard version changes, new model and/or product releases, product differences between differing manufacturers, software changes, BIOS flashes, firmware upgrades, or the like. Any computer system has risks of security vulnerabilities that cannot be completely prevented or mitigated. AMD assumes no obligation to update or
  otherwise correct or revise this information. However, AMD reserves the right to revise this information and to make changes from time to time to the content hereof without obligation of AMD to notify any person of such revisions or changes. THIS INFORMATION IS PROVIDED "AS IS." AMD MAKES NO REPRESENTATIONS OR WARRANTIES WITH RESPECT TO THE CONTENTS HEREOF AND ASSUMES NO RESPONSIBILITY FOR ANY INACCURACIES, ERRORS, OR OMISSIONS THAT MAY APPEAR IN THIS INFORMATION. AMD SPECIFICALLY
  DISCLAIMS ANY IMPLIED WARRANTIES OF NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR ANY PARTICULAR PURPOSE. IN NO EVENT WILL AMD BE LIABLE TO ANY
  PERSON FOR ANY RELIANCE, DIRECT, INDIRECT, SPECIAL, OR OTHER CONSEQUENTIAL DAMAGES ARISING FROM THE USE OF ANY INFORMATION CONTAINED HEREIN, EVEN IF
  AMD IS EXPRESSLY ADVISED OF THE POSSIBILITY OF SUCH DAMAGES. 

  ##################################
  AUTOMOTIVE APPLICATIONS DISCLAIMER
  ##################################


  AUTOMOTIVE PRODUCTS (IDENTIFIED AS "XA" IN THE PART NUMBER) ARE NOT WARRANTED FOR USE IN THE DEPLOYMENT OF AIRBAGS OR FOR USE IN APPLICATIONS
  THAT AFFECT CONTROL OF A VEHICLE ("SAFETY APPLICATION") UNLESS THERE IS A SAFETY CONCEPT OR REDUNDANCY FEATURE CONSISTENT WITH THE ISO 26262 AUTOMOTIVE SAFETY STANDARD ("SAFETY DESIGN"). CUSTOMER SHALL, PRIOR TO USING OR DISTRIBUTING ANY SYSTEMS THAT INCORPORATE PRODUCTS, THOROUGHLY TEST SUCH SYSTEMS FOR SAFETY PURPOSES. USE OF PRODUCTS IN A SAFETY APPLICATION WITHOUT A SAFETY DESIGN IS FULLY AT THE RISK OF CUSTOMER, SUBJECT ONLY TO APPLICABLE LAWS AND REGULATIONS GOVERNING LIMITATIONS ON PRODUCT LIABILITY.

  #########
  Copyright
  #########


  © Copyright 2023 Advanced Micro Devices, Inc. AMD, the AMD Arrow logo, Ryzen, Vitis AI, and combinations thereof are trademarks of Advanced Micro Devices,
  Inc. AMBA, AMBA Designer, Arm, ARM1176JZ-S, CoreSight, Cortex, PrimeCell, Mali, and MPCore are trademarks of Arm Limited in the US and/or elsewhere. PCI, PCIe, and PCI Express are trademarks of PCI-SIG and used under license. OpenCL and the OpenCL logo are trademarks of Apple Inc. used by permission by Khronos. Other product names used in this publication are for identification purposes only and may be trademarks of their respective companies.

