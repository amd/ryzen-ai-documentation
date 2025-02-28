.. Heading guidelines
..     # with overline, for parts
..     * with overline, for chapters
..     =, for sections
..     -, for subsections
..     ^, for subsubsections
..     “, for paragraphs

###########################
Server Interface (REST API)
###########################

The ``lemonade`` SDK server interface allows your application to load an LLM on Ryzen AI hardware in a process, and then communicate with this process using standard ``REST`` APIs. This allows applications written in any language (C#, JavaScript, Python, C++, etc.) to easily integrate with Ryzen AI LLMs.

Server interfaces are used across the LLM ecosystem because they allow for no-code plug-and-play between the higher level of the application stack (GUIs, agents, RAG, etc.) with the LLM and hardware that have been abstracted by the server. 

For example, open source projects such as `Open WebUI <https://github.com/open-webui/open-webui>`_ and `LM Eval <https://github.com/EleutherAI/lm-evaluation-harness>`_ have out-of-box support for connecting to a variety of server interfaces, which allow users to quickly start working with LLMs in a GUI or run a variety of validation tasks, respectively.

************
Server Setup
************

The fastest way to set up the server is with the ``lemonade server installer``.

#. Make sure your system has the Ryzen AI 1.3 driver installed: :ref:`install-npu-drivers`.
#. Download and install ``Lemonade_Server_Installer.exe`` from the `latest TurnkeyML release <https://github.com/onnx/turnkeyml/releases>`_.
#. Launch the server by double-clicking the ``lemonade_server`` shortcut added to your desktop.

************
Server Usage
************

The ``lemonade`` server provides the following OpenAI-compatible endpoints:

- POST ``/api/v0/chat/completions`` - Chat Completions (messages to completions)
- GET ``/api/v0/models`` - List available models

Please refer to the `server specification <https://github.com/aigdat/genai/blob/main/docs/lemonade/server_spec.md>`_ document in the lemonade repository for details about the request and response formats for each endpoint. 

The `OpenAI API documentation <https://platform.openai.com/docs/api-reference/streaming>`_ also has code examples for integrating streaming completions into an application. 

Open WebUI Demo
===============

The best way to experience the ``lemonade`` server is to try it with an OpenAI-compatible application, like Open WebUI.  

Instructions:

1. In a terminal, install Open WebUI:

  #. conda create -n webui python=3.11
  #. pip install open-webui
  #. open-webui serve

2. Open http://localhost:8080/ in your browser to launch the UI.
3. In the UI:

  #. Go to ``Settings -> Connections -> Add Connection``
  #. Set http://localhost:8000/api/v0 as the URL, "-" as the key, and press save.

Done! You are now able to run Open WebUI with Hybrid models. Feel free to choose any of the available "-Hybrid" models on the model selection menu.

**********
Next Steps
**********

- Visit the :ref:`supported-llms` table to see the set of hybrid checkpoints that can be used with the server.
- Check out the `lemonade server specification <https://github.com/aigdat/genai/blob/main/docs/lemonade/server_spec.md>`_ to learn more about supported features.
- Try out your ``lemonade server`` install with any application that uses the OpenAI chat completions API.


..
  ------------
  #####################################
  License
  #####################################
  
  Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
