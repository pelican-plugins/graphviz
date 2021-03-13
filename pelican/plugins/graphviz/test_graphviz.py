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
    r'<div class="%s"><img src="data:image/svg\+xml;base64,[0-9a-zA-Z+/]+" /></div>'
)


class TestGraphviz(unittest.TestCase):
    """Class for testing the URL output of the Graphviz plugin"""

    def setUp(self, block_start="..graphviz", image_class="graphviz"):

        # Set the paths for the input (content) and output (html) files
        self.output_path = mkdtemp(prefix=TEST_DIR_PREFIX)
        self.content_path = mkdtemp(prefix=TEST_DIR_PREFIX)

        # Configuration setting for the Pelican process
        settings = {
            "PATH": self.content_path,
            "OUTPUT_PATH": self.output_path,
            "PLUGINS": [graphviz],
            "CACHE_CONTENT": False,
            "GRAPHVIZ_BLOCK_START": block_start,
            "GRAPHVIZ_IMAGE_CLASS": image_class,
        }

        # Store the image_class in self, since it will be needed in the
        # test_output method defined below
        self.image_class = image_class

        # Create the article file
        fid = open(os.path.join(self.content_path, "%s.md" % TEST_FILE_STEM), "w")
        # Write header
        fid.write("Title: %s\nDate: 1970-01-01\n" % TEST_FILE_STEM)
        # Write Graphviz block
        fid.write(
            """
%s dot
digraph G {
  graph [rankdir = LR];
  Hello -> World
}
"""
            % block_start
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
        fid = open(os.path.join(self.output_path, "%s.html" % TEST_FILE_STEM))
        found = False
        # Iterate over the lines and look for the HTML element corresponding
        # to the generated Graphviz figure
        for line in fid.readlines():
            if re.search(GRAPHVIZ_RE % self.image_class, line):
                found = True
                break
        assert found


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
