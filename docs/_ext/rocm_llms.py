"""LLM-friendly documentation export without the full rocm_docs.projects stack."""

from __future__ import annotations

from pathlib import Path

from sphinx.application import Sphinx
from sphinx.config import Config
from sphinx.errors import ExtensionError

MARKDOWN_BUTTON = {
    "type": "link",
    "text": ".md",
    "tooltip": "Download as Markdown",
    "icon": "fas fa-file-code",
    "label": "download-markdown-button",
}

PDF_BUTTON = {
    "type": "javascript",
    "javascript": "window.print()",
    "text": ".pdf",
    "tooltip": "Print to PDF",
    "icon": "fas fa-file-pdf",
    "label": "download-pdf-button",
}


def _setup_markdown_builder(app: Sphinx, _: Config) -> None:
    if not app.config.rocm_docs_generate_llms:
        return
    try:
        import sphinx_markdown_builder  # noqa: F401
    except ImportError as err:
        raise ExtensionError(
            "rocm_docs_generate_llms is enabled but "
            "'sphinx-markdown-builder' is not installed. Install it with: "
            "pip install rocm-docs-core[llms]"
        ) from err
    app.setup_extension("sphinx_markdown_builder")


def _generate_llms(app: Sphinx, exception: object) -> None:
    if not app.config.rocm_docs_generate_llms:
        return
    from rocm_docs import llms

    llms.generate_llms_full(app, exception)
    _write_per_page_markdown(app, exception)


def _write_per_page_markdown(app: Sphinx, exception: object) -> None:
    if exception is not None:
        return
    if getattr(app.builder, "format", "") != "html":
        return

    from rocm_docs.llms import (
        _build_markdown_renderer,
        _is_excluded_from_fulltext,
        _render_page_markdown,
        _resolve_base_url,
    )

    base_url = _resolve_base_url(app)
    builder, writer = _build_markdown_renderer(app)
    saved_http_base = app.config.markdown_http_base
    app.config.markdown_http_base = base_url
    written = 0
    try:
        for docname in sorted(app.project.docnames):
            if docname.startswith("_") or _is_excluded_from_fulltext(app, docname):
                continue
            doctree = app.env.get_and_resolve_doctree(docname, app.builder)
            markdown = _render_page_markdown(builder, writer, doctree, docname)
            out_path = Path(app.outdir) / f"{docname}.md"
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(markdown, encoding="utf-8")
            written += 1
    finally:
        app.config.markdown_http_base = saved_http_base

    if written:
        app.info(f"Wrote {written} per-page Markdown files", type="llms")


def _markdown_download_url(pagename: str) -> str:
    return f"{pagename.rsplit('/', 1)[-1]}.md"


def _add_download_buttons(
    app: Sphinx, pagename: str, templatename: str, context: dict, doctree
) -> None:
    if not app.config.rocm_docs_generate_llms:
        return

    md_button = {
        **MARKDOWN_BUTTON,
        "url": _markdown_download_url(pagename),
    }
    header_buttons = context.setdefault("header_buttons", [])
    header_buttons.append(
        {
            "type": "group",
            "tooltip": "Download this page",
            "icon": "fas fa-download",
            "buttons": [md_button, dict(PDF_BUTTON)],
            "label": "download-buttons",
        }
    )


def setup(app: Sphinx) -> dict[str, bool]:
    app.add_config_value(
        "rocm_docs_generate_llms",
        default=False,
        rebuild="html",
        types=bool,
    )
    app.add_config_value(
        "rocm_docs_llms_base_url",
        default="",
        rebuild="html",
        types=str,
    )
    app.add_config_value(
        "rocm_docs_llms_full_exclude",
        default=[],
        rebuild="html",
        types=list,
    )
    app.connect("config-inited", _setup_markdown_builder, priority=300)
    app.connect("html-page-context", _add_download_buttons, priority=502)
    app.connect("build-finished", _generate_llms)
    return {"parallel_read_safe": True, "parallel_write_safe": True}
