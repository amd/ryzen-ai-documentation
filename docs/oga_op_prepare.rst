#######################################
Preparing Operators for OGA/ONNX Models
#######################################

Currently Ryzen AI supports many popular LLMs in hybrid or NPU only flow. For all these models the required operators are already compiled and available in the Ryzen AI runtime. All these models can be directly runs on Ryzen AI without any preparation needed. In some cases the user can change (fine-tune) the model weights which does not introduce any new operator shapes requirement. For those fine tuned model follow the model prepretation page to prepare the model which can be run on Ryzen Ai runtime with precompiled operators. However, there are sometimes some architecture changes required new operator shape which maynot be available in the ryzenAI runtime. This page provides a receipe to compile operators which are not available in the Ryzen AI runtime. Currently this flow is experimental and depending on the amount of architectural change the milage can vary.  

All the OGA models are currently based on Onnx Runtime GenAi model builder architecture support. So this op preparation flow assumes models are already supported in ONNXRuntime Gen AI (or very close variant of it). 

