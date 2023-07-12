###################
Model Compatibility
###################

In the Ryzen AI workflow, the quantized model is converted into ONNX format for deployment. Currently, the IPU supports a subset of ONNX operators. However, with the Vitis AI ONNX Execution Provider, the neural network is automatically partitioned into multiple subgraphs. The subgraph(s) containing IPU-supported operators are executed on the IPU, while the remaining subgraph(s) containing IPU-incompatible operators are executed on the CPU. This "Model Parallel" deployment technique across the CPU and IPU is fully automated and managed by the Vitis AI ONNX Execution Provider, and it is transparent to the end-user.

The current list of IPU-supported ONNX operators is as below:

- Add
- And
- Average pool
- BatchNorm
- Clip
- Concat
- Conv
- ConvTranspose
- Gemm
- GlobalAveragePool
- GlobalMaxPool
- Identity
- LayerNorm
- LSTM
- Max
- MaxPool
- Mul
- Pad
- Prelu
- Relu
- Resize
- RNN
- Sigmoid
- Slice
- Softmax
- Split
- Squeeze
- Unsqueeze
- Upsample
- Spacetodepth

..
  ------------

  #####################################
  License
  #####################################

  Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
