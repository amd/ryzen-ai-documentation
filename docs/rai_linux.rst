:orphan:

************************
Ryzen AI Linux Installer
************************

This guide provides instructions for using Ryzen AI 1.4 on Linux for model compilation and followed by running inference on windows.

Prerequisites
~~~~~~~~~~~~~
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


Linux Installation
~~~~~~~~~~~~~~~~~~

- Download the RyzenAI Software Linux installer :download:`ryzen_ai-1.4.0.tgz <https://account.amd.com/en/forms/downloads/ryzenai-eula-public-xef.html?filename=ryzen_ai-1.4.0-ea.tgz>`.

- Extract the .tgz using the following command: 

.. code-block::

    tar -xvzf ryzen_ai-1.4.0.tgz -C <TARGET DIR>

- Installer will prompted to agree to the EULA. Re-run after reading the EULA:

.. code-block::

    cd <TARGET DIR>
    ./install_ryzen_ai_1_4.sh -a yes -p <TARGET PATH TO VENV> -l

- Activate the virtual environment:  

.. code-block::

   source <PATH TO VENV>/bin/activate



Alternatively, you can use **Docker based installer** for Ryzen AI software :download:`ryzen_ai_docker-1.4.0-ea_2025_02_21_3914.tgz <https://account.amd.com/en/forms/downloads/ryzenai-eula-public-xef.html?filename=ryzen_ai_docker-1.4.0-ea_2025_02_21_3914.tgz>`.


- Installation command:

.. code-block::

    gunzip -c ryzen_ai_docker-1.4.0-ea_2025_02_21_3914.tgz | docker load


After installing on Linux machine, the process for model compilation on Linux is similar to that on Windows.

Once the model has been successfully compiled on your Linux machine, proceed to copy the entire working directory to a Windows machine that operates on an STX-based system.

Prior to running the model on the Windows machine, ensure that all required prerequisites are satisfied as listed in the :doc:`inst` documentation page.

To deploy the model on the Windows machine, follow the instructions provided in the :doc:`modelrun` page.


