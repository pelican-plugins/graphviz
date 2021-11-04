"""Unit testing suite for the Graphviz plugin"""

# Copyright (C) 2015, 2021  Rafael Laboissière <rafael@laboissiere.net>
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
    r'<{0} class="{1}"><img src="data:image/svg\+xml;base64,[0-9a-zA-Z+=]+"></{0}>'
)
GRAPHVIZ_RE_XML = r'<svg width="\d+pt" height="\d+pt"'


class TestGraphviz(unittest.TestCase):
    """Class for testing the URL output of the Graphviz plugin"""

    def setUp(
        self,
        block_start="..graphviz",
        image_class="graphviz",
        html_element="div",
        compress=True,
    ):

        # Set the paths for the input (content) and output (html) files
        self.output_path = mkdtemp(prefix=TEST_DIR_PREFIX)
        self.content_path = mkdtemp(prefix=TEST_DIR_PREFIX)

        # Configuration setting for the Pelican process
        settings = {
            "PATH": self.content_path,
            "OUTPUT_PATH": self.output_path,
            "PLUGINS": [graphviz],
            "CACHE_CONTENT": False,
            "GRAPHVIZ_HTML_ELEMENT": html_element,
            "GRAPHVIZ_BLOCK_START": block_start,
            "GRAPHVIZ_IMAGE_CLASS": image_class,
            "GRAPHVIZ_COMPRESS": compress,
        }

        # Store the image_class and the html_element in self, since they will be
        # needed in the test_output method defined below
        self.image_class = image_class
        self.html_element = html_element

        # Create the article file
        fid = open(os.path.join(self.content_path, "{}.md".format(TEST_FILE_STEM)), "w")
        # Write header
        fid.write("Title: {}\nDate: 1970-01-01\n".format(TEST_FILE_STEM))
        # Write Graphviz block
        fid.write(
            """
{} dot
digraph G {{
  graph [rankdir = LR];
  Hello -> World
}}
""".format(
                block_start
            )
        )
        fid.close()

        # Run the Pelican instance
        self.settings = read_settings(override=settings)
        pelican = Pelican(settings=self.settings)
        pelican.run()

    def tearDown(self):
        """Clean up the temporary directories"""
        rmtree(self.output_path)
        rmtree(self.content_path)

    def test_output(self):
        """Test for default values of the configuration variables"""
        # Open the output HTML file
        content = open(
            os.path.join(self.output_path, "{}.html".format(TEST_FILE_STEM))
        ).read()
        found = False
        # Iterate over the lines and look for the HTML element corresponding
        # to the generated Graphviz figure
        for line in content.splitlines():
            if self.settings["GRAPHVIZ_COMPRESS"]:
                if re.search(
                    GRAPHVIZ_RE.format(self.html_element, self.image_class), line
                ):
                    found = True
                    break
            else:
                if re.search(GRAPHVIZ_RE_XML, line):
                    found = True
                    break
        assert found, content


class TestGraphvizHtmlElement(TestGraphviz):
    """Class for exercising the configuration variable GRAPHVIZ_HTML_ELEMENT"""

    def setUp(self):
        """Initialize the configuration"""
        TestGraphviz.setUp(self, html_element="span")

    def test_output(self):
        """Test for GRAPHVIZ_HTML_ELEMENT setting"""
        TestGraphviz.test_output(self)


class TestGraphvizBlockStart(TestGraphviz):
    """Class for exercising the configuration variable GRAPHVIZ_BLOCK_START"""

    def setUp(self):
        """Initialize the configuration"""
        TestGraphviz.setUp(self, block_start="==foobar")

    def test_output(self):
        """Test for GRAPHVIZ_BLOCK_START setting"""
        TestGraphviz.test_output(self)


class TestGraphvizImageClass(TestGraphviz):
    """Class for exercising configuration variable GRAPHVIZ_IMAGE_CLASS"""

    def setUp(self):
        """Initialize the configuration"""
        TestGraphviz.setUp(self, image_class="foo")

    def test_output(self):
        """Test for GRAPHVIZ_IMAGE_CLASS setting"""
        TestGraphviz.test_output(self)


class TestGraphvizImageNoCompress(TestGraphviz):
    """Class for exercising configuration variable GRAPHVIZ_COMPRESS"""

    def setUp(self):
        """Initialize the configuration"""
        TestGraphviz.setUp(self, compress=False)

    def test_output(self):
        """Test for GRAPHVIZ_COMPRESS setting"""
        TestGraphviz.test_output(self)
