####################
ONNX End-to-End Flow
####################

The ONNX end-to-end flow provides a framework to create and add pre/post-processing operators to the pre-trained model which enables end-to-end model inference using Vitis AI Execution Provider. The feature is built by leveraging the ONNX Runtime feature `ONNXRuntime-Extensions <https://onnxruntime.ai/docs/extensions/>`_. Typical pre-processing (or post-processing) tasks, such as resize, normalization, etc can be expressed as custom operators. The pretrained model can then be extended by absorbing these custom operators. The resulting model that contains the pre/post-processing operations can then be run on NPU. This helps improve end-to-end latency and facilitates PC power saving by reducing CPU utilization.

An example showing the ONNX end-to-end flow can be found `here <https://github.com/amd/RyzenAI-SW/tree/main/example/onnx-e2e>`_.
