#######################################
Compiling Operators for OGA/ONNX Models
#######################################

Ryzen AI currently supports many popular LLMs in both hybrid and NPU-only flows. For these models, the required operators are already compiled and included in the Ryzen AI runtime. Such models can be run directly on Ryzen AI without any additional preparation.

When users fine-tune these models, only the weights change and no new operator shapes are introduced. In that case, follow the Model Preparation steps to prepare the model, which will run on the Ryzen AI runtime using the precompiled operators.

However, in cases where architectural changes introduce new operator shapes not available in the Ryzen AI runtime, additional operator compilation is required. This page provides a recipe to compile operators that are not already present in the runtime. **This flow is experimental, and results may vary depending on the extent of the architectural changes**.

All OGA models are currently based on the ONNX Runtime GenAI Model Builder (https://github.com/microsoft/onnxruntime-genai/tree/main/src/python/py/models#current-support) architecture. Therefore, this operator compilation flow assumes the models are supported by ONNX Runtime GenAI (or a close variant).


 

