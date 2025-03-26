:orphan:

##########################
Ryzen AI Software on Linux
##########################

This guide provides instructions for using Ryzen AI 1.4 on Linux for model compilation and followed by running inference on Windows.

*************
Prerequisites
*************
The following are the recommended system configuration for RyzenAI Linux installer

.. list-table:: 
   :widths: 25 25 
   :header-rows: 1

   * - Dependencies
     - Version Requirement
   * - Ubuntu
     - 22.04
   * - RAM
     - 32GB or Higher
   * - CPU cores
     - >= 8 
   * - Python
     - 3.10 or Higher


*************************
Installation Instructions
*************************

Option 1: Local Installation
============================

- Download the Ryzen AI Software Linux installer: :download:`ryzen_ai-1.4.0.tgz <https://account.amd.com/en/forms/downloads/ryzenai-eula-public-xef.html?filename=ryzen_ai-1.4.0-ea.tgz>`.

- Extract the .tgz using the following command: 

.. code-block::

    tar -xvzf ryzen_ai-1.4.0.tgz -C <TARGET DIR>

- The installer will prompt to agree to the EULA. Re-run after reading the EULA:

.. code-block::

    cd <TARGET DIR>
    ./install_ryzen_ai_1_4.sh -a yes -p <TARGET PATH TO VENV> -l

- Activate the virtual environment:  

.. code-block::

   source <PATH TO VENV>/bin/activate


Option 2: Docker Image
======================

- Download the Ryzen AI Software Docker image: :download:`ryzen_ai_docker-1.4.0-ea_2025_02_21_3914.tgz <https://account.amd.com/en/forms/downloads/ryzenai-eula-public-xef.html?filename=ryzen_ai_docker-1.4.0-ea_2025_02_21_3914.tgz>`.

- Load the Docker image:

.. code-block::

    gunzip -c ryzen_ai_docker-1.4.0-ea_2025_02_21_3914.tgz | docker load


******************
Usage Instructions
******************

The process for model compilation on Linux is similar to that on Windows. Refer to the instructions provided in the :doc:`modelrun` page for complete details.

Once the model has been successfully compiled on your Linux machine, proceed to copy the entire working directory to a Windows machine that operates on an STX-based system.

Prior to running the compiled model on the Windows machine, ensure that all required prerequisites are satisfied as listed in the :doc:`inst` page.
