Graphviz: A Plugin for Pelican
==============================

[![Build Status](https://img.shields.io/github/workflow/status/pelican-plugins/graphviz/build)](https://github.com/pelican-plugins/graphviz/actions)
[![PyPI Version](https://img.shields.io/pypi/v/pelican-graphviz)](https://pypi.org/project/pelican-graphviz/)
![License](https://img.shields.io/pypi/l/pelican-graphviz?color=blue)

Graphviz is a Pelican plugin that allows the inclusion of [Graphviz][] images using the Markdown markup format. The code for the Graphviz figure is included as a block in the article’s source, and the image is embedded in HTML using the Base64 format.

[Graphviz](https://www.graphviz.org)


Installation
------------

This plugin can be installed via:

    python -m pip install pelican-graphviz

Graphviz must be installed on the system, otherwise this plugin will be deactivated. Graphviz can be installed on Debian-based systems via:

    sudo aptitude install graphviz


Usage
-----

In the Markdown source, the Graphviz code must be inserted as an individual block (i.e., separated from the rest of the material by blank lines), like the following:

```markdwon
..graphviz dot
digraph G {
  graph [rankdir = LR];
  Hello -> World
}
```

This will insert an image in your article like this:

![figure](hello-world.png)

The block must start with `..graphviz` (this is configurable — see below). The word `dot` in the first line indicates the program that will be run to produce the image. The available programs are: `dot`, `neato`, `twopi`, `circo`, `fdp`, `sfdp`, and `patchwork` (see the [Graphviz documentation][] for details). The Graphviz code must start in the second line of the block. Notice that *newlines are not allowed inside the Graphviz block*.

[Graphviz documentation]: https://www.graphviz.org/documentation/


Styling with CSS
----------------

The image is generated in HTML with an `<img>` element inside an HTML element (by default a `<div>`, but this is configurable — see below). The latter has class `graphviz` (this is also configurable — see below). A possible CSS styling would be:

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


Configuration
-------------

The following variables can be set in the Pelican settings file:

- `GRAPHVIZ_HTML_ELEMENT`: The HTML inside which the generated Graphviz image is inserted (defaults to `'div'`; another sensible possibility would be `'span'`).

- `GRAPHVIZ_IMAGE_CLASS`: Class of the `<div>` element including the generated Graphviz image (defaults to `'graphviz'`).

- `GRAPHVIZ_BLOCK_START`: Starting tag for the Graphviz block in Markdown (defaults to `'..graphviz'`).


Output Image Format
-------------------

The format of the embedded image is SVG, and there is currently no way to change it. This format was chosen over others (like PNG) for two reasons. First, the generated SRC string in Base64 seem to be shorter for SVG than for PNG. Second, the image will be available in the browser in a high-quality vectorized format. As a caveat, notice that this choice may prevent display in browsers lacking proper SVG support.


Alternatives
------------

An alternative to this plugin would be the [graphviz tag][] provided by the [Liquid Tags plugin][]. The Graphviz plugin differs from Liquid Tags in many aspects. First, Liquid Tags uses the the syntax `{% graphviz { <program> […] } %}`, while the Graphviz plugin uses the Markdown extension syntax `..graphviz <program> […]`. As regards the output, these are the differences:

[graphviz tag]: https://github.com/pelican-plugins/liquid-tags/blob/main/pelican/plugins/liquid_tags/graphviz.py
[Liquid Tags plugin]: https://github.com/pelican-plugins/liquid-tags

- Both plugins output an element with `class="graphviz"`. However, only the Graphviz plugin allows to change the class name through a configuration variable (`GRAPHVIZ_IMAGE_CLASS`).
- Liquid Tags encodes the image as `src="data:image/png;base64,[…]"`, while the Graphviz plugin encodes it as `src="data:image/svg+xml;base64,[…]"`. This has two impacts. First, the size of the produced HTML code is much smaller for the Graphviz plugin. For instance, the a base64 string for the Graphviz code `digraph graphname {a -> b -> c; b -> d;}` is four times smaller. Second, the output of Liquid Tags is pixelated, while the output of the Graphviz plugin is vectorial and the resulting web page can be zoomed without loss of quality.
- Liquid Tags outputs the Graphviz image inside a `<span>`, while the choice of the container element is free for the Graphviz plugin.


To-Do
-----

Contributions that make this plugin work with [reStructuredText][] content would be welcome.

[reStructuredText]: https://docutils.sourceforge.io/rst.html


Contributing
------------

Contributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].

To start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.

[existing issues]: https://github.com/pelican-plugins/graphviz/issues
[Contributing to Pelican]: https://docs.getpelican.com/en/latest/contribute.html


License
-------

Copyright © 2015, 2021  Rafael Laboissière <rafael@laboissiere.net>

This project is licensed under the AGPL-3.0 license.
