"""Markdown Graphviz plugin for Pelican"""

## Copyright (C) 2015  Rafael Laboissiere
##
## This program is free software: you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by the
## Free Software Foundation, either version 3 of the License, or (at your
## option) any later version.
##
## This program is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License along
## with this program.  If not, see http://www.gnu.org/licenses/.

import os
import subprocess

import logging
logger = logging.getLogger (__name__)

from pelican import signals

from .mdx_graphviz import GraphvizExtension

def initialize (pelicanobj):
    """Initialize the Markdown Graphviz plugin"""
    pelicanobj.settings.setdefault ('MD_GRAPHVIZ_BLOCK_START', '..graphviz')
    pelicanobj.settings.setdefault ('MD_GRAPHVIZ_IMAGE_CLASS', 'graphviz')

    config = {'block-start':
                  pelicanobj.settings.get ('MD_GRAPHVIZ_BLOCK_START'),
              'image-class':
                  pelicanobj.settings.get ('MD_GRAPHVIZ_IMAGE_CLASS')}

    pelicanobj.settings ['MD_EXTENSIONS'].append (GraphvizExtension (config))

def register ():
    """Register the Markdown Graphviz plugin with Pelican"""
    if subprocess.call (['dot', '-V'], stderr = open (os.devnull, 'w')) == 0:
        signals.initialized.connect (initialize)
    else:
        logger.warning ('The dot program from Graphviz is not available. '
                        'The Graphviz plugin is deactivated.')
