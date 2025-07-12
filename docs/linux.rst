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

Use the commands below to install Python 3.10.x along with certain dependecies

.. code-block::

  sudo apt-get install python3.10
  sudo apt-get install python3.10-venv

Once you have correct Ubuntu distribution and Python installed locally, you can proceed with NPU drivers installation

.. _install-driver:

*******************
Install NPU Drivers
*******************
- Download the NPU driver package from this link :download:`NPU Driver <https://mkmartifactory.amd.com:8443/artifactory/atg-cvml-generic-local/builds/Linux-ipu/Release/IPU_RC3_25.06.24/jenkins-CVML-Release-linux-ipu-sw-release-40/build/>`

- RyzenAI linux driver package contains 
   - XRT Package
      - xrt_202520.2.20.41_24.04-amd64-base.deb
      - xrt_202520.2.20.41_24.04-amd64-base-dev.deb
      - xrt_202520.2.20.41_24.04-amd64-npu.deb

   - NPU driver package
      - xrt_plugin.2.20.250102.3.rel_24.04-amd64-amdxdna.deb

- Follow the instructions below to install NPU driver package

.. code-block::

   $ sudo apt reinstall --fix-broken -y ./xrt_202520.2.20.41_24.04-amd64-base.deb
   $ sudo apt reinstall --fix-broken -y ./xrt_202520.2.20.41_24.04-amd64-base-dev.deb
   $ sudo apt reinstall --fix-broken -y ./xrt_202520.2.20.41_24.04-amd64-npu.deb 
   $ sudo apt reinstall --fix-broken -y ./xrt_plugin.2.20.250102.3.rel_24.04-amd64-amdxdna.deb
   $ source /opt/xilinx/xrt/setup.sh




.. _install-bundled:

*************************
Install Ryzen AI Software
*************************
- Download the RyzenAI for Linux package :download:`ryzen-ai-1.5.0.tgz <https://xcoartifactory/ui/native/vaiml-installers-prod-local/installers/rai-1.5.0/latest/lnx64/ryzen_ai-1.5.0.tgz>`
- Navigate to the downloaded path and follow the below steps

.. code-block::

   tar -xvzf ryzen_ai-1.5.0.tgz 
   cd ryzen-ai-1.5.0

- Install RyzenAI package at your desired target path

.. code-block::

   ./install_ryzen_ai_1_5.sh -a yes -p <TARGET-PATH/venv>
   source <TARGET-PATH/venv>/bin/activate

- This will successfully install RyzenAI and activate the Virtual environment at your targeted location. You can verify by running the command "pip list"
