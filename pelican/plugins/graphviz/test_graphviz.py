"""Unit testing suite for the Graphviz plugin."""

# Copyright (C) 2015, 2021, 2023, 2025  Rafael Laboissière <rafael@laboissiere.net>
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

import os
import re
from shutil import rmtree
from tempfile import mkdtemp
import unittest

from pelican import Pelican
from pelican.settings import read_settings

from . import graphviz

TEST_FILE_STEM = "test"
TEST_DIR_PREFIX = "pelicantests."
GRAPHVIZ_RE = (
    r'<{0} class="{1}"><img alt="{2}" '
    r'src="data:image/svg\+xml;base64,[0-9a-zA-Z+=]+"></{0}>'
)

GRAPHVIZ_RE_XML = r'<svg width="\d+pt" height="\d+pt"'


class TestGraphviz(unittest.TestCase):
    """Class for testing the URL output of the Graphviz plugin."""

    def setUp(
        self,
        input_md_block_start="..graphviz",
        input_options=None,
        input_digraph_id="G",
        settings=None,
        expected_compressed=True,
        expected_html_element="div",
        expected_image_class="graphviz",
        expected_alt_text="G",
    ):
        """Set up the test environment."""
        # Set the paths for the input (content) and output (html) files
        self.output_path = mkdtemp(prefix=TEST_DIR_PREFIX)
        self.content_path = mkdtemp(prefix=TEST_DIR_PREFIX)

        # Save input
        self.input_md_block_start = input_md_block_start
        self.input_options = input_options
        self.input_digraph_id = input_digraph_id

        # Save expected output
        self.expected_compressed = expected_compressed
        self.expected_html_element = expected_html_element
        self.expected_image_class = expected_image_class
        self.expected_alt_text = expected_alt_text

        # Configuration setting for the Pelican process
        self.settings = {
            "PATH": self.content_path,
            "OUTPUT_PATH": self.output_path,
            "PLUGINS": [graphviz],
            "CACHE_CONTENT": False,
        }
        if settings is not None:
            self.settings.update(settings)

    def test_md(self):
        options_string = ""
        if self.input_options:
            kvs = ",".join(f'{k}="{v}"' for k, v in self.input_options.items())
            options_string = f"[{kvs}]"

        # Create the article file
        with open(os.path.join(self.content_path, f"{TEST_FILE_STEM}.md"), "w") as fid:
            # Write header
            fid.write(f"Title: {TEST_FILE_STEM}\nDate: 1970-01-01\n")
            # Write Graphviz block
            md_input = f"""
{self.input_md_block_start} {options_string} dot
digraph{f" {self.input_digraph_id}" if self.input_digraph_id else ""} {{
  graph [rankdir = LR];
  Hello -> World
}}
"""
            fid.write(md_input)

        self.run_pelican()
        self.assert_expected_output()

    def run_pelican(self):
        settings = read_settings(override=self.settings)
        pelican = Pelican(settings=settings)
        pelican.run()

    def assert_expected_output(self):
        """Test for default values of the configuration variables."""
        # Open the output HTML file
        with open(os.path.join(self.output_path, f"{TEST_FILE_STEM}.html")) as fid:
            content = fid.read()
            found = False
            # Iterate over the lines and look for the HTML element corresponding
            # to the generated Graphviz figure
            for line in content.splitlines():
                if self.expected_compressed:
                    if re.search(
                        GRAPHVIZ_RE.format(
                            self.expected_html_element,
                            self.expected_image_class,
                            self.expected_alt_text,
                        ),
                        line,
                    ):
                        found = True
                        break
                elif re.search(GRAPHVIZ_RE_XML, line):
                    found = True
                    break
            assert found, content

    def tearDown(self):
        """Tidy up the test environment."""
        rmtree(self.output_path)
        rmtree(self.content_path)


class TestGraphvizHtmlElement(TestGraphviz):
    """Class for exercising the configuration variable GRAPHVIZ_HTML_ELEMENT."""

    def setUp(self):
        """Initialize the configuration."""
        super().setUp(
            settings={"GRAPHVIZ_HTML_ELEMENT": "span"},
            expected_html_element="span",
        )


class TestGraphvizBlockStart(TestGraphviz):
    """Class for exercising the configuration variable GRAPHVIZ_BLOCK_START."""

    def setUp(self):
        """Initialize the configuration."""
        super().setUp(
            settings={"GRAPHVIZ_BLOCK_START": "==foobar"},
            input_md_block_start="==foobar",
        )


class TestGraphvizImageClass(TestGraphviz):
    """Class for exercising configuration variable GRAPHVIZ_IMAGE_CLASS."""

    def setUp(self):
        """Initialize the configuration."""
        super().setUp(
            settings={"GRAPHVIZ_IMAGE_CLASS": "foo"}, expected_image_class="foo"
        )


class TestGraphvizImageNoCompress(TestGraphviz):
    """Class for exercising configuration variable GRAPHVIZ_COMPRESS."""

    def setUp(self):
        """Initialize the configuration."""
        super().setUp(settings={"GRAPHVIZ_COMPRESS": False}, expected_compressed=False)


class TestGraphvizLocallyOverrideConfiguration(TestGraphviz):
    """Class for exercising the override of a configuration variable."""

    def setUp(self):
        """Initialize the configuration."""
        super().setUp(
            input_options={"html-element": "span"},
            expected_html_element="span",
        )


class TestGraphvizAltText(TestGraphviz):
    """Class for exercising configuration variable GRAPHVIZ_ALT_TEXT."""

    def setUp(self):
        """Initialize the configuration."""
        super().setUp(
            input_digraph_id="G",
            settings={"GRAPHVIZ_ALT_TEXT": "foo"},
            expected_alt_text="G",
        )


class TestGraphvizAltTextWithoutID(TestGraphviz):
    """Class for testing the case where the Graphviz element has no id."""

    def setUp(self):
        """Initialize the configuration."""
        super().setUp(
            input_digraph_id=None,
            settings={"GRAPHVIZ_ALT_TEXT": "foo"},
            expected_alt_text="foo",
        )


class TestGraphvizAltTextViaOption(TestGraphviz):
    """Class for testing the alternative text given via the alt-text option."""

    def setUp(self):
        """Initialize the configuration."""
        text = "A wonderful graph"
        super().setUp(
            input_options={"alt-text": text},
            expected_alt_text=text,
        )
