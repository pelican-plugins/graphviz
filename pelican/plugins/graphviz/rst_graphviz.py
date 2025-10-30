"""reStructuredText extension for the Graphviz plugin for Pelican."""

# Copyright (C) 2025  Mark Shroyer <mark@shroyer.name>
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Affero Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/.

import html
from typing import ClassVar
import xml.etree.ElementTree as ET

from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.parsers.rst.directives import unchanged

from .run_graphviz import append_compressed_img, run_graphviz


def truthy(argument: str) -> bool:
    """Parse a "truthy" RST option.

    Applies permissive conventions to interpret to interpret "truthy"-looking
    strings as True, or False otherwise.
    """
    return argument.lower() in ("yes", "true", "on", "1")


def make_graphviz_directive(config):
    """Build a graphviz directive."""

    class GraphvizDirective(Directive):
        """RST directive for embedded Graphviz."""

        required_arguments = 1
        option_spec: ClassVar = {
            "image-class": unchanged,
            "html-element": unchanged,
            "compress": truthy,
            "alt-text": unchanged,
        }
        has_content = True
        _config = config

        def run(self):
            config = self._config.copy()
            config.update(self.options)

            program = self.arguments[0]
            code = "\n".join(self.content)

            output = run_graphviz(program, code, format="svg")

            elt = ET.Element(config["html-element"])
            elt.set("class", config["image-class"])

            if config["compress"]:
                append_compressed_img(config, output, elt)
                img_html = ET.tostring(elt, encoding="unicode", method="html")
            else:
                svg = output.decode("utf-8")
                start = svg.find("<svg")
                tag = html.escape(config["html-element"], quote=True)
                class_ = html.escape(config["image-class"], quote=True)
                img_html = f'<{tag} class="{class_}">{svg[start:]}</{tag}>'

            svg_node = nodes.raw("", img_html, format="html")
            container = nodes.container("", svg_node, classes=["graphviz"])
            return [container]

    return GraphvizDirective
