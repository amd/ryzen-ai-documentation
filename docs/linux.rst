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

*********************
NPU drivers for Linux
*********************
- Download the NPU driver package from this link :download:`NPU Driver <https://amdcloud.sharepoint.com/sites/EdgeML/Shared%20Documents/Forms/AllItems.aspx?id=%2Fsites%2FEdgeML%2FShared%20Documents%2FIPU%2FStrix%2Flinux&viewid=64125ca9%2D13b9%2D4d73%2Dbe5a%2D08008740e650&p=true&ga=1>`

- RyzenAI linux driver package contains 
   - XRT Package:
      - xrt_202520.2.20.41_24.04-amd64-base.deb
      - xrt_202520.2.20.41_24.04-amd64-base-dev.deb
      - xrt_202520.2.20.41_24.04-amd64-npu.deb
   - NPU driver package:
      - xrt_plugin.2.20.250102.3.rel_24.04-amd64-amdxdna.deb

- Follow the instructions below to install NPU driver package

.. code-block::

   $ sudo apt reinstall --fix-broken -y ./xrt_202520.2.20.41_24.04-amd64-base.deb
   $ sudo apt reinstall --fix-broken -y ./xrt_202520.2.20.41_24.04-amd64-base-dev.deb
   $ sudo apt reinstall --fix-broken -y ./xrt_202520.2.20.41_24.04-amd64-npu.deb 
   $ sudo apt reinstall --fix-broken -y ./xrt_plugin.2.20.1773d9b_ubuntu24.04-x86_64-amdxdna.deb




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
