############
Installation
############


Vitis AI Quantizer, which is part of the complete Vitis AI toolchain, requires the installation of a Docker container on the host server.

Host Server Requirement
~~~~~~~~~~~~~~~~~~~~~~~

The Vitis AI Docker container can be installed on Ubuntu 20.04, CentOS 7.8, 7.9, 8.1, and RHEL 8.3, 8.4. The developers working on Windows 11 can use `WSL <https://learn.microsoft.com/en-us/windows/wsl/install>`_ for installing Vitis AI docker. 


Docker Container Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Multiple versions of the Docker container are available, each tailored to specific frameworks and GPU support.  

Examples: 


- PyTorch docker without AMD GPU acceleration support: 

.. code-block:: 

    docker pull xilinx/vitis-ai-pytorch-cpu:latest

- PyTorch docker with AMD GPU acceleration support:

.. code-block:: 

    docker pull xilinx/vitis-ai-pytorch-rocm:latest

- TensorFlow 2 docker without AMD GPU acceleration support:

.. code-block:: 
  
    docker pull xilinx/vitis-ai-tensorflow2-cpu:latest

- TensorFlow 2 docker with AMD GPU acceleration support:

.. code-block:: 

   docker pull xilinx/vitis-ai-tensorflow2-rocm:latest
   


Next, you can now start the Vitis AI Docker using the following commands:

.. code-block:: 

    cd <Vitis-AI install path>/Vitis-AI
    ./docker_run.sh xilinx/vitis-ai-<pytorch|opt-pytorch|tensorflow2>-<cpu|rocm>:latest
    
    


..
  ------------

  #####################################
  License
  #####################################

 Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
