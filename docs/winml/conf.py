#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Sphinx configuration for the Windows ML RTD subproject.
# Register this subproject in Read the Docs admin with:
#   Path for .readthedocs.yaml: docs/winml/.readthedocs.yaml

import os
import sys
import urllib.parse

sys.path.insert(0, os.path.abspath("../_ext"))
sys.path.insert(0, os.path.abspath(".."))

project = "Windows ML on Ryzen AI"
copyright = "2023-2025, Advanced Micro Devices, Inc"
author = "Advanced Micro Devices, Inc"

version = "1.7"
release = ""
html_last_updated_fmt = "%b %d, %Y"

html_baseurl = os.environ.get(
    "READTHEDOCS_CANONICAL_URL",
    "https://ryzenai.docs.amd.com/projects/WinML/en/latest/",
)
html_context = {}
if os.environ.get("READTHEDOCS", "") == "True":
    html_context["READTHEDOCS"] = True

extensions = [
    "rocm_llms",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.mathjax",
    "linuxdoc.rstFlatTable",
    "notfound.extension",
    "sphinx_copybutton",
]

templates_path = ["_templates", "../_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

master_doc = "index"
language = "en"
pygments_style = "sphinx"
todo_include_todos = False

source_suffix = {
    ".rst": "restructuredtext",
}

html_theme = "rocm_docs_theme"
html_theme_options = {
    "link_main_doc": False,
    "flavor": "local",
    "use_download_button": False,
    "article_header_end": ["article-header-buttons.html"],
}

html_static_path = ["../_static"]
html_css_files = ["../_static/llm-table.css"]


def setup(app):
    app.add_css_file("llm-table.css")


rocm_docs_generate_llms = True
rocm_docs_llms_base_url = "https://ryzenai.docs.amd.com/projects/WinML/en/latest/"

intersphinx_mapping = {
    "ryzenai": ("https://ryzenai.docs.amd.com/en/latest/", None),
}

if "READTHEDOCS" in os.environ:
    components = urllib.parse.urlparse(os.environ["READTHEDOCS_CANONICAL_URL"])
    notfound_urls_prefix = components.path
