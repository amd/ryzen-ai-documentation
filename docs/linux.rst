#########################
Linux Installation Instructions
#########################

Ryzen AI for linux supports compiling the AI models and running on AMD processor- Neural Processing Unit (NPU). 

*************
Prerequisites
*************

.. list-table::
   :widths: 25 25
   :header-rows: 1

   * - Dependencies
     - Version Requirement
   * - Ubuntu Distribution
     - Ubuntu 24.04 LTS
   * - Python
     - 3.10.x

Once you have correct Ubuntu distribution and Python installed locally, you can download and extract below packages

***********
NPU drivers
***********
- Download the NPU drivers from this link :download:`NPU Driver <https://mkmartifactory.amd.com:8443/artifactory/atg-cvml-generic-local/builds/Linux-ipu/Release/IPU_RC3_25.06.24/jenkins-CVML-Release-linux-ipu-sw-release-40/build/>`

- To add steps to extract and install

*****************
RyzenAI for Linux
*****************
- Download the RyzenAI for Linux package :download:`ryzen-ai-1.5.0.tgz <https://xcoartifactory/artifactory/vaiml-installers-prod-local/installers/rai-1.5.0/ryzenai_1.5.0_2025_07_09_7550/lnx64/ryzen_ai-1.5.0.tgz>`
- Navigate to the downloaded path and follow the below steps

.. code-block::

   tar -xvzf ryzen_ai-1.5.0.tgz 
   cd ryzen-ai-1.5.0

- Install RyzenAI package at your desired target path

.. code-block::

   ./install_ryzen_ai_1_4.sh -a yes -p <TARGET-PATH/venv> -l
   source <TARGET-PATH/venv>/bin/activate

- This will successfully install RyzenAI and activate the Virtual environment at your targeted location. You can verify by running the command "pip list"
