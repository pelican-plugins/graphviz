"""Markdown Graphviz plugin for Pelican"""

# Copyright (C) 2015, 2021  Rafael Laboissière
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see http://www.gnu.org/licenses/.

import logging
import os
import subprocess

from pelican import signals

from .mdx_graphviz import GraphvizExtension

logger = logging.getLogger(__name__)


def initialize(pelicanobj):
    """Initialize the Markdown Graphviz plugin"""
    pelicanobj.settings.setdefault("GRAPHVIZ_BLOCK_START", "..graphviz")
    pelicanobj.settings.setdefault("GRAPHVIZ_IMAGE_CLASS", "graphviz")
    pelicanobj.settings.setdefault("GRAPHVIZ_HTML_ELEMENT", "div")
    pelicanobj.settings.setdefault("GRAPHVIZ_COMPRESS", True)

    config = {
        "block-start": pelicanobj.settings.get("GRAPHVIZ_BLOCK_START"),
        "image-class": pelicanobj.settings.get("GRAPHVIZ_IMAGE_CLASS"),
        "html-element": pelicanobj.settings.get("GRAPHVIZ_HTML_ELEMENT"),
        "compress": pelicanobj.settings.get("GRAPHVIZ_COMPRESS"),
    }

    if isinstance(
        pelicanobj.settings.get("MD_EXTENSIONS"), list
    ):  # pelican 3.6.3 and earlier
        pelicanobj.settings["MD_EXTENSIONS"].append(GraphvizExtension(config))
    else:
        pelicanobj.settings["MARKDOWN"].setdefault("extensions", []).append(
            GraphvizExtension(config)
        )


def register():
    """Register the Markdown Graphviz plugin with Pelican"""
    if subprocess.call(["dot", "-V"], stderr=open(os.devnull, "w")) == 0:
        signals.initialized.connect(initialize)
    else:
        logger.warning(
            "The dot program from Graphviz is not available. "
            "The Graphviz plugin is deactivated."
        )
