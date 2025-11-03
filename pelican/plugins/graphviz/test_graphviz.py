"""Unit testing suite for the Graphviz plugin."""

# Copyright (C) 2015, 2021, 2023, 2025  Rafael Laboissière <rafael@laboissiere.net>
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

import os
import re
from shutil import rmtree
from tempfile import mkdtemp
import unittest

from bs4 import BeautifulSoup, Tag

from pelican import Pelican
from pelican.settings import read_settings

from . import graphviz

TEST_FILE_STEM = "test"
TEST_DIR_PREFIX = "pelicantests."
DIMENSION_ATTR_RE = re.compile(r"\d+pt")


class TestGraphviz(unittest.TestCase):
    """Class for testing the URL output of the Graphviz plugin."""

    def setUp(
        self,
        config={},
        settings={},
        expected={},
    ):
        """Set up the test environment."""
        # Set the paths for the input (content) and output (html) files
        self.output_path = mkdtemp(prefix=TEST_DIR_PREFIX)
        self.content_path = mkdtemp(prefix=TEST_DIR_PREFIX)

        # Input configuration
        self.config = {
            "md_block_start": "..graphviz",
            "options": None,
            "digraph_id": "G",
        }
        self.config.update(config)

        # Settings for the Pelican process
        self.settings = {
            "PATH": self.content_path,
            "OUTPUT_PATH": self.output_path,
            "PLUGINS": [graphviz],
            "CACHE_CONTENT": False,
        }
        self.settings.update(settings)

        # Properties of the expected output
        self.expected = {
            "compressed": True,
            "html_element": "div",
            "image_class": "graphviz",
            "alt_text": "G",
        }
        self.expected.update(expected)

    def test_md(self):
        options_string = ""
        if self.config["options"]:
            kvs = ",".join(
                f'{k}="{v}"' for k, v in self.config["options"].items()
            )
            options_string = f"[{kvs}]"

        # Create the article file
        with open(
                os.path.join(self.content_path, f"{TEST_FILE_STEM}.md"),
                "w"
        ) as fid:
            # Write header
            fid.write(f"Title: {TEST_FILE_STEM}\nDate: 1970-01-01\n")
            # Write Graphviz block
            fid.write(f"""
{self.config["md_block_start"]} {options_string} dot
digraph{f" {self.config['digraph_id']}" if self.config["digraph_id"] else ""} {{
  graph [rankdir = LR];
  Hello -> World
}}
""")

        self.run_pelican()
        self.assert_expected_output()

    def test_rst(self):
        options_string = ""
        if self.config["options"]:
            options_string = "\n".join(
                f"   :{k}: {v}" for k, v in self.config["options"].items()
            )

        with open(
                os.path.join(self.content_path, f"{TEST_FILE_STEM}.rst"),
                "w"
        ) as fid:
            rst_input = f"""\
{TEST_FILE_STEM}
################
:date: 1970-01-01
:slug: {TEST_FILE_STEM}

.. graphviz:: dot
{options_string}

   digraph{f" {self.config['digraph_id']}" if self.config["digraph_id"] else ""} {{
     graph [rankdir = LR];
     Hello -> World
   }}
"""
            fid.write(rst_input)

        self.run_pelican()
        self.assert_expected_output()

    def run_pelican(self):
        settings = read_settings(override=self.settings)
        pelican = Pelican(settings=settings)
        pelican.run()

    def assert_expected_output(self):
        """Test for default values of the configuration variables."""
        # Open the output HTML file
        with open(
                os.path.join(self.output_path, f"{TEST_FILE_STEM}.html")
        ) as fid:
            # Keep content as a string so we can see full content in output
            # from failed asserts.
            content = fid.read()
            soup = BeautifulSoup(content, "html.parser")
            if self.expected["compressed"]:
                elt = soup.find(
                    self.expected["html_element"],
                    class_=self.expected["image_class"],
                )
                assert isinstance(elt, Tag), content

                img = elt.find("img", attrs={"alt": self.expected["alt_text"]})
                assert img is not None, content
            else:
                svg = soup.find("svg")
                assert isinstance(svg, Tag), content

                for attr in ["width", "height"]:
                    assert attr in svg.attrs
                    assert DIMENSION_ATTR_RE.fullmatch(str(svg.attrs[attr]))

    def tearDown(self):
        """Tidy up the test environment."""
        rmtree(self.output_path)
        rmtree(self.content_path)


class TestGraphvizHtmlElement(TestGraphviz):
    """Class for exercising the configuration variable GRAPHVIZ_HTML_ELEMENT."""

    def setUp(self):
        """Initialize the configuration."""
        value = "span"
        super().setUp(
            settings={"GRAPHVIZ_HTML_ELEMENT": value},
            expected={"html_element": value},
        )


class TestGraphvizBlockStart(TestGraphviz):
    """Class for exercising the configuration variable GRAPHVIZ_BLOCK_START.

    Because the reStructredText implementation does not allow configuring the
    directive name using GRAPHVIZ_BLOCK_START, test_rst() is essentially a
    no-op for this test case.
    """

    def setUp(self):
        """Initialize the configuration."""
        value = "==foobar"
        super().setUp(
            config={"md_block_start": value},
            settings={"GRAPHVIZ_BLOCK_START": value},
        )


class TestGraphvizImageClass(TestGraphviz):
    """Class for exercising configuration variable GRAPHVIZ_IMAGE_CLASS."""

    def setUp(self):
        """Initialize the configuration."""
        value = "foo"
        super().setUp(
            settings={"GRAPHVIZ_IMAGE_CLASS": value},
            expected={"image_class": value},
        )


class TestGraphvizImageNoCompress(TestGraphviz):
    """Class for exercising configuration variable GRAPHVIZ_COMPRESS."""

    def setUp(self):
        """Initialize the configuration."""
        value = False
        super().setUp(
            settings={"GRAPHVIZ_COMPRESS": value},
            expected={"compressed": value},
        )


class TestGraphvizImageCompressOptionNo(TestGraphviz):
    """Class for exercising the compress option set to "no".

    Ensures that a "no" compress option is parsed as False and overrides the
    setting.

    """

    def setUp(self):
        """Initialize the configuration."""
        super().setUp(
            config={"options": {"compress": "no"}},
            settings={"GRAPHVIZ_COMPRESS": True},
            expected={"compressed": False},
        )


class TestGraphvizImageCompressOptionYes(TestGraphviz):
    """Class for exercising the compress option set to "yes".

    Ensures that a "yes" compress option is parsed as True and overrides the
    setting.

    """

    def setUp(self):
        """Initialize the configuration."""
        super().setUp(
            config={"options": {"compress": "yes"}},
            settings={"GRAPHVIZ_COMPRESS": False},
            expected={"compressed": True},
        )


class TestGraphvizLocallyOverrideConfiguration(TestGraphviz):
    """Class for exercising the override of a configuration variable."""

    def setUp(self):
        """Initialize the configuration."""
        value = "span"
        super().setUp(
            config={"options": {"html-element": value}},
            expected={"html_element": value},
        )


class TestGraphvizAltText(TestGraphviz):
    """Class for exercising configuration variable GRAPHVIZ_ALT_TEXT."""

    def setUp(self):
        """Initialize the configuration."""
        value = "G"
        super().setUp(
            config={"digraph_id": value},
            settings={"GRAPHVIZ_ALT_TEXT": "foo"},
            expected={"alt_text": value},
        )


class TestGraphvizAltTextWithoutID(TestGraphviz):
    """Class for testing the case where the Graphviz element has no id."""

    def setUp(self):
        """Initialize the configuration."""
        value = "foo"
        super().setUp(
            config={"digraph_id": None},
            settings={"GRAPHVIZ_ALT_TEXT": value},
            expected={"alt_text": value},
        )


class TestGraphvizAltTextViaOption(TestGraphviz):
    """Class for testing the alternative text given via the alt-text option."""

    def setUp(self):
        """Initialize the configuration."""
        text = "A wonderful graph"
        super().setUp(
            config={"options": {"alt-text": text}},
            expected={"alt_text": text},
        )
