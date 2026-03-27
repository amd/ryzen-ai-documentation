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

The Lemonade SDK offers a server interface that allows your application to load an LLM on Ryzen AI hardware in a process, and then communicate with this process using standard ``REST`` APIs. This allows applications written in any language (C#, JavaScript, Python, C++, etc.) to easily integrate with Ryzen AI LLMs.

Server interfaces are used across the LLM ecosystem because they allow for no-code plug-and-play between the higher level of the application stack (GUIs, agents, RAG, etc.) with the LLM and hardware that have been abstracted by the server. For more information, see the `Understanding local LLM Servers Guide <https://lemonade-server.ai/docs/server/concepts/>`_.

For example, open source projects such as `Open WebUI <#open-webui-demo>`_ have out-of-box support for connecting to a variety of server interfaces, which in turn allows users to quickly start working with LLMs in a GUI.


************
Server Setup
************

Lemonade Server can be installed via the Lemonade Server Installer executable by following these steps:

1. Make sure your system has the recommended Ryzen AI driver installed as described in :ref:`install-driver`.
2. Download and install ``Lemonade_Server_Installer.exe`` from the `latest Lemonade release <https://github.com/lemonade-sdk/lemonade/releases>`_.
3. Launch the server by double-clicking the ``lemonade_server`` shortcut added to your desktop.

For a visual walkthrough of this process, watch our Lemonade Introductory Video:

.. raw:: html

   <div style="text-align: center; margin: 20px 0;">
       <iframe width="560" height="315" 
               src="https://www.youtube.com/embed/mcf7dDybUco?si=J9ocgcRF_LNY0s8E" 
               title="Lemonade Introductory Video" 
               frameborder="0" 
               allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
               allowfullscreen>
       </iframe>
   </div>

See the `Lemonade Server Documentation <https://lemonade-server.ai/docs/>`_ for more details.

************
Server Usage
************

The Lemonade Server provides the following OpenAI-compatible endpoints:

- POST ``/api/v1/chat/completions`` - Chat Completions (messages to completions)
- POST ``/api/v1/completions`` - Text Completions (prompt to completion)
- POST ``/api/v1/responses`` - Chat Completions (prompt|messages -> event)
- GET ``/api/v1/models`` - List available models

Please refer to the `server specification <https://lemonade-server.ai/docs/server/server_spec/>`_ document for details about the request and response formats for each endpoint. 

The `OpenAI API documentation <https://platform.openai.com/docs/guides/streaming-responses?api-mode=chat>`_ also has code examples for integrating streaming completions into an application. 

Supported Applications
======================

The Lemonade Server supports a variety of applications that can connect to it using the OpenAI API. Some of the applications that have been tested with Lemonade Server can be found at `Lemonade Server Apps <https://lemonade-server.ai/docs/server/apps/>`_.

A short list of applications that have been tested with Lemonade Server includes:

.. |open-webui| image:: https://raw.githubusercontent.com/lemonade-sdk/assets/refs/heads/main/partner_logos/openwebui.jpg
   :width: 60px
   :target: https://lemonade-server.ai/docs/server/apps/open-webui/
   :alt: Open WebUI

.. |continue| image:: https://raw.githubusercontent.com/lemonade-sdk/assets/refs/heads/main/partner_logos/continue_dev.png
   :width: 60px
   :target: https://lemonade-server.ai/docs/server/apps/continue/
   :alt: Continue

.. |gaia| image:: https://raw.githubusercontent.com/lemonade-sdk/assets/refs/heads/main/partner_logos/gaia.ico
   :width: 60px
   :target: https://github.com/amd/gaia
   :alt: Gaia

.. |anythingllm| image:: https://raw.githubusercontent.com/lemonade-sdk/assets/refs/heads/main/partner_logos/anything_llm.png
   :width: 60px
   :target: https://lemonade-server.ai/docs/server/apps/anythingLLM/
   :alt: AnythingLLM

.. |ai-dev-gallery| image:: https://raw.githubusercontent.com/lemonade-sdk/assets/refs/heads/main/partner_logos/ai_dev_gallery.webp
   :width: 60px
   :target: https://lemonade-server.ai/docs/server/apps/ai-dev-gallery/
   :alt: AI Dev Gallery

.. |lm-eval| image:: https://raw.githubusercontent.com/lemonade-sdk/assets/refs/heads/main/partner_logos/lm_eval.png
   :width: 60px
   :target: https://lemonade-server.ai/docs/server/apps/lm-eval/
   :alt: LM-Eval

.. |codegpt| image:: https://raw.githubusercontent.com/lemonade-sdk/assets/refs/heads/main/partner_logos/codegpt.jpg
   :width: 60px
   :target: https://lemonade-server.ai/docs/server/apps/codeGPT/
   :alt: CodeGPT

.. |ai-toolkit| image:: https://raw.githubusercontent.com/lemonade-sdk/assets/refs/heads/main/partner_logos/ai_toolkit.png
   :width: 60px
   :target: https://github.com/lemonade-sdk/lemonade/blob/main/docs/server/apps/ai-toolkit.md
   :alt: AI Toolkit

|open-webui| |continue| |gaia| |anythingllm| |ai-dev-gallery| |lm-eval| |codegpt| |ai-toolkit|


**********
Next Steps
**********

- See `Lemonade Server Examples <https://lemonade-server.ai/docs/server/apps/>`_ to find applications that have been tested with Lemonade Server.
- Check out the `Lemonade Server specification <https://lemonade-server.ai/docs/server/server_spec/>`_ to learn more about supported features.
- Try out your Lemonade Server install with any application that uses the OpenAI chat completions API.

..
  ------------
  #####################################
  License
  #####################################
  
  Ryzen AI is licensed under `MIT License <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ . Refer to the `LICENSE File <https://github.com/amd/ryzen-ai-documentation/blob/main/License>`_ for the full license text and copyright notice.
