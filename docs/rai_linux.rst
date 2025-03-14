****************************
Ryzen AI Linux Compile Flow
****************************

BF16 models (CNN or Transformer) require processing power in terms of core count and memory, depending on model size. If a larger model cannot be compiled on a Windows machine due to hardware limitations (e.g., insufficient RAM), an alternative Linux-based compilation flow is supported.

- Download the RyzenAI Software Linux installer :download:`ryzen_ai-1.4.0.tgz <https://account.amd.com/en/forms/downloads/ryzenai-eula-public-xef.html?filename=ryzen_ai-1.4.0-ea.tgz>`.

- Download install script to your Ubuntu (22.04) host

.. code-block::

    tar -xvzf ryzen_ai-1.4.0.tgz -C <EXTRACT TO DIR>
    cd <TARGET DIR>
    chmod a+x install_ryzen_ai_1_4.sh
    cd <TARGET DIR>
    ./install_ryzen_ai_1_4.sh -a yes -p <TARGET PATH TO VENV> -l
    source <TARGET PATH TO VENV>/bin/activate

- Use Docker to install the Ryzen AI Software :download:`ryzen_ai_docker-1.4.0-ea_2025_02_21_3914.tgz <https://account.amd.com/en/forms/downloads/ryzenai-eula-public-xef.html?filename=ryzen_ai_docker-1.4.0-ea_2025_02_21_3914.tgz>`.

- Installation command:

.. code-block::

    gunzip -c ryzen_ai_docker-1.4.0-ea_2025_02_21_3914.tgz | docker load
