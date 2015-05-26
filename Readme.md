# Graphviz plugin for Pelican


## Description

This plugins allows the inclusion of [Graphviz](http://www.graphviz.org/)
images using the Markdown text markup.  The code for the Graphviz figure is
included as a block in the article's source and the image is embedded in
HTML using the Base64 format.


## Installation

Graphviz must be installed in the system, otherwise this plugin will be
deactivated.  In Debian-based systems, do:

    sudo aptitude install graphviz

You might install this plugin directly from Github along with your website
sources.  At the top-level directory, do, for instance:

    mkdir plugins-extra 
    git clone https://github.com/rlaboiss/pelican-md-graphviz.git plugins-extra/graphviz

In `pelicanconf.py`, add `'plugins-extra'` to `PLUGIN_PATHS` and
`'graphviz'` to `PLUGINS` (see the Pelican
[documentation](http://docs.getpelican.com/en/3.5.0/plugins.html#how-to-use-plugins)
for details about configuring your plugins).


## Usage

In the Markdown source, the Graphviz code must be inserted an individual
block (i.e. separated from the rest of the material by blank lines), like
the following:

```markdwon
..graphviz dot
digraph G {
  graph [rankdir = LR];
  Hello -> World
}
```

This will insert an image in your article like this:

![figure](hello-world.png)

The block must start with `..graphviz` (although this is configurable, see
below).  The word `dot` in the first line indicates the program that will
be run for producing the image.  The available programs are `dot`, `neato`,
`twopi`, `circo`, `fdp`, `sfdp`, and `patchwork`.  (see the Graphviz
[documentation](http://www.graphviz.org/Documentation.php) for details).
The Graphviz code must start in the second line of the block.  Notice that
__newlines are not allowed inside the Graphviz block__.


## Styling with CSS

The image is generated in HTML with an `<img>` element inside a `<div>`
element.  The latter has class `graphviz` (although this is configurable,
see below).  A possible CSS styling would be:

```css
div.graphviz  {
    margin: 10px;
}
div.graphviz img {
    display: block;
    padding: 5px;
    margin-left: auto;
    margin-right: auto;
    text-align: center;
    border-style: solid;
    border-width: 1px;
    border-color: rgb(192, 177, 177);
    -webkit-border-radius: 5px;
}
``` 


## Configuration

The following variables can be set in the Pelican configuration file:

- `MD_GRAPHVIZ_IMAGE_CLASS`: Class of the `<div>` element including the
  yielding Graphviz image (defaults to `graphviz`).

- `MD_GRAPHVIZ_BLOCK_START`: Starting tag for the Graphviz block in
  Markdown (defaults to `..graphviz`).


## Format of the output image

The format of the embedded image is SVG and there is currently no way to
change it.  This format was chosen over others (like PNG) for two reasons.
First, the generated SRC string in Base64 seem to be shorter for SVG than
for PNG.  Second, the image will be available in the browser as a
hi-quality vectorized format.  As a caveat, notice that this choice may
prevent a display in browser lacking proper SVG support.


## Alternatives

An alternative to this plugin would be the
[Liquid Tags extension](http://blog.dornea.nu/2014/11/13/using-graphviz-with-pelican-and-liquid-tags/)
available at Github.  However, this extension needs a patch to the
[liquid_tags](https://github.com/dorneanu/pelican-plugins/tree/master/liquid_tags)
plugin, which complicates its installation.


## Author

Copyright (C) 2015  Rafael Laboissiere (<rafael@laboissiere.net>)

Released under the GNU Affero Public License, version 3 or later.  No
warranties.
