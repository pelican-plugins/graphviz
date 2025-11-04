"""Markdown extension for the Graphviz plugin for Pelican."""

# Copyright (C) 2015, 2021, 2023, 2025  Rafael Laboissière
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

import re
import xml.etree.ElementTree as ET

from markdown import Extension
from markdown.blockprocessors import BlockProcessor

from .run_graphviz import append_base64_img, run_graphviz


class GraphvizProcessor(BlockProcessor):
    """Block processor for the Graphviz Markdown Extension."""

    def __init__(self, md_parser, config):
        """Class initialization."""
        self.config = config
        BlockProcessor.__init__(self, md_parser)

    def test(self, parent, block):
        """Tell the Markdown processor that this block is for us."""
        return block.startswith(self.config["block-start"])

    def run(self, parent, blocks):
        """Do the actual formatting."""
        # The following line is extremely important, otherwise it will
        # reiterate ad infinitum
        block = blocks.pop(0)

        # Get a local copy of the configuration hash
        config = self.config.copy()

        m = re.match(
            r"^{}\s+(?:\[(.*)\]\s+)?([^\s]+)".format(config["block-start"]),
            block.split("\n")[0],
        )
        if m:
            # Gather local configuration values
            if m.group(1):
                for keyval in re.findall(
                    r'\s*([^=\s]*)\s*=\s*([^"=,\s]*|"[^"]*")\s*(?:,|$)',
                    m.group(1),
                ):
                    key = keyval[0]
                    val = keyval[1].strip('"')
                    if val in ("yes", "no"):
                        config[key] = val == "yes"
                    else:
                        config[key] = val
            # Get the graphviz program name and the input code
            program = m.group(2)
            code = "\n".join(block.split("\n")[1:])
        else:
            return

        output = run_graphviz(program, code, image_format="svg")

        # Set HTML element
        elt = ET.SubElement(parent, config["html-element"])

        # Set CSS class
        elt.set("class", config["image-class"])

        # Cope with compression
        if config["compress"]:
            append_base64_img(output, config, elt)
        else:
            svg = output.decode()
            start = svg.find("<svg")
            elt.text = "\n" + svg[start:]


class GraphvizExtension(Extension):
    """Markdow extension for Graphviz blocks."""

    def __init__(self, config):
        """Initialize the GraphvizExtension class."""
        self.config = config

    def extendMarkdown(self, md):
        """Add an instance of GraphvizProcessor to BlockParser."""
        md.registerExtension(self)
        md.parser.blockprocessors.register(
            GraphvizProcessor(md.parser, self.config), "graphviz", 200
        )
