####################
PyTorch Quantization
####################


Enabling Quantization
~~~~~~~~~~~~~~~~~~~~~

To enable Vitis AI Pytorch Quantization, acvitate the conda environment inside Vitis AI Pytorch Docker container:

.. code-block::

     conda activate vitis-ai-pytorch
     
 
Post-Training Quantization
~~~~~~~~~~~~~~~~~~~~~~~~~~

Post-Training Quantization requires the following files:

 1. model.pth : Pre-trained PyTorch model, generally pth file.
 2. model.py : A Python script including float model definition.
 3. calibration dataset: A subset of the training dataset containing 100 to 1000 images.

A complete example of Post-Training Quantization is available in `Vitis AI GitHub <https://github.com/Xilinx/Vitis-AI/blob/v3.0/src/vai_quantizer/vai_q_pytorch/example/resnet18_quant.py>`__


Vitis AI Quantization APIs
%%%%%%%%%%%%%%%%%%%%%%%%%%

Vitis AI provides ``pytorch_nndct`` module with Quantization related APIs. 

1. Import the vai_q_pytorch module.

.. code-block:: 

    from pytorch_nndct.apis import torch_quantizer, dump_xmodel

2. Generate a quantizer with quantization needed input and get the converted model.

.. code-block::

   input = torch.randn([batch_size, 3, 224, 224])
   quantizer = torch_quantizer(quant_mode, model, (input))
   quant_model = quantizer.quant_model

3. Forward a neural network with the converted model.

.. code-block:: 

    acc1_gen, acc5_gen, loss_gen = evaluate(quant_model, val_loader, loss_fn)

4. Output the quantization result and deploy the model.

.. code-block:: 
 
    quantizer.export_quant_config()

5. Export the quantized model for deployment.

.. code-block::

    quantizer.export_onnx_model()
    
    
Quantization Output
%%%%%%%%%%%%%%%%%%%

If this quantization command runs successfully, two important files are generated in the output directory ``./quantize_result``.

  • ``<model>.onnx``: Quantized ONNX model
  • ``Quant_info.json``: Quantization steps of tensors. Retain this file for evaluating quantized models.


Hardware-Aware Quantization
%%%%%%%%%%%%%%%%%%%%%%%%%%%

To enable hardware-aware quantization provide the ``target`` to the IPU specific archietecture as follows: 

.. code-block::

   quantizer = torch_quantizer(quant_mode=quant_mode,
                               module=model,
                               input_args=(input),
                               device=device,
                               quant_config_file=config_file,
                               target=target)
                               
The ``target`` of current version of IPU is ``AMD_AIE2_Nx4_Overlay_cfg0``


Partial Quantization
%%%%%%%%%%%%%%%%%%%%

Partial quantization can be enabled by using ``QuantStab`` and ``DeQuantStub`` operator from the ``pytorch_nndct`` library. In the following example, we are quantizing the layers ``subm0`` and ``subm2``, but not the ``subm1``. 

.. code-block::

   from pytorch_nndct.nn import QuantStub, DeQuantStub

   class WholeModule(torch.nn.module):
      def __init__(self,...):
         self.subm0 = ...
         self.subm1 = ...
         self.subm2 = ...

         # define QuantStub/DeQuantStub submodules
         self.quant = QuantStub()
         self.dequant = DeQuantStub()
         
      def forward(self, input):
          input = self.quant(input) # begin of part to be quantized
          output0 = self.subm0(input)
          output0 = self.dequant(output0) # end of part to be quantized

          output1 = self.subm1(output0)

          output1 = self.quant(output1) # begin of part to be quantized
          output2 = self.subm2(output1)
          output2 = self.dequant(output2) # end of part to be quantized


Fast Finetuing
%%%%%%%%%%%%%%

After post-training quantization, there is usually a small accuracy loss. If the accuracy loss is large, a fast-finetuning approach, which is based on the `AdaQuant Algorithm <https://arxiv.org/abs/2006.10518>`__, can be tried instead of the quantization aware training. The fast finetuning uses a small unlabeled data to calibrate the activations and finetuning the weights. 


.. code-block:: 

  # fast finetune model or load finetuned parameter before test
  
  if fast_finetune == True:
      ft_loader, _ = load_data(
                 subset_len=5120,
                 train=False,
                 batch_size=batch_size,
                 sample_method='random',
                 data_dir=args.data_dir,
                 model_name=model_name)
                 
  if quant_mode == 'calib':
      quantizer.fast_finetune(evaluate, (quant_model, ft_loader, loss_fn))
  elif quant_mode == 'test':
      quantizer.load_ft_param()


Quantization Aware Training
~~~~~~~~~~~~~~~~~~~~~~~~~~~

An example of Quantization Aware Training is available at the `Vitis Github <https://github.com/Xilinx/Vitis-AI/blob/v3.0/src/vai_quantizer/vai_q_pytorch/example/resnet18_qat.py>`__ 

General approaches are:

1. If some non-module operations are needed to be quantized, convert them into module operations. For example, ResNet18 uses ``+`` operator to add two tensors, which can be replaced by ``pytorch_nndct.nn.modules.functional.Add``. 

2. If some modules are calles multiple times, uniqify them by defining multiple such modules and call them separately in the foward pass.

3. Insert ``QuantStub`` and ``DeQuantStub``. Any sub-network from QuantStub to DeQuantStub in a forward pass will be quantized. Multiple QuantStub-DeQuantStub pairs are allowed.

4. Create Quantizer module from the ``QatProcessor`` library


.. code-block::

   from pytorch_nndct import QatProcessor
   qat_processor = QatProcessor(model, inputs, bitwidth=8)
   quantized_model = qat_processor.trainable_model()
   optimizer = torch.optim.Adam(
                     quantized_model.parameters(),
                     lr,
                      weight_decay=weight_decay)

5. For testing after the training, get the deployable model: 

.. code-block::

   output_dir = 'qat_result'
   deployable_model = qat_processor.to_deployable(quantized_model,output_dir)
   validate(val_loader, deployable_model, criterion, gpu)
   
6. Export ONNX model for prediction:

.. code-block::

     qat_processor.export_onnx_model()
     
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

