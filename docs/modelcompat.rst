###################
Model Compatibility
###################

In the Ryzen AI workflow, the quantized model is converted into ONNX format for deployment. Currently, the IPU supports a subset of ONNX operators. However, with the Vitis AI ONNX Execution Provider (VAI EP), the neural network is automatically partitioned into multiple subgraphs. The subgraph(s) containing IPU-supported operators are executed on the IPU, while the remaining subgraph(s) containing IPU-incompatible operators are executed on the CPU. This *Model Parallel* deployment technique across the CPU and IPU is fully automated. VAI EP manages it and is transparent to the end-user.

The current list of the IPU-supported ONNX operators is as follows:

- Abs
- Add
- And
- Argmax
- Argmin
- Average pool_2D
- BatchNorm
- Channel Shuffle
- Clip
- Concat
- Convolution
- ConvTranspose
- Depthwise_Convolution
- Div
- Elu
- Equal
- Exp
- Fully-Connected
- Gemm
- GlobalAveragePool
- GlobalMaxPool
- Greater
- GreaterOrEqual
- Gstiling
- Hard-Sigmoid
- Hard-Swish
- Identity
- LayerNorm
- LeakyRelu
- Less
- LessOrEqual
- LSTM
- MatMul
- Max
- Min
- MaxPool
- Mul
- Neg
- Not
- Or
- Pad: constant or symmetric
- Pixel-Shuffle
- Pixel-Unshuffle
- Prelu
- ReduceMax
- ReduceMin
- ReduceMean
- ReduceSum
- Relu
- Reshape
- Resize
- RNN
- Sigmoid
- Slice
- Softmax
- SpaceToDepth
- Sqrt
- Split
- Squeeze
- Strided-Slice
- Sub
- Tanh
- Unsqueeze
- Upsample

..
  ------------

  #####################################
  License
  #####################################

  Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
