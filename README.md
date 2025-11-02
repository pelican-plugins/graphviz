Graphviz: A Plugin for Pelican
==============================

[![Build Status](https://img.shields.io/github/actions/workflow/status/pelican-plugins/graphviz/main.yml?branch=main)](https://github.com/pelican-plugins/graphviz/actions)
[![PyPI Version](https://img.shields.io/pypi/v/pelican-graphviz)](https://pypi.org/project/pelican-graphviz/)
[![Downloads](https://img.shields.io/pypi/dm/pelican-graphviz)](https://pypi.org/project/pelican-graphviz/)
[![License](https://img.shields.io/pypi/l/pelican-graphviz?color=blue)](https://www.gnu.org/licenses/agpl-3.0.en.html)

Graphviz is a Pelican plugin enables [Graphviz][] images to be included using the Markdown or reStructuredText markup format. The Graphviz code for the image is included as a block in the article’s source. In the HTML output file, the Graphviz image can appear as either a `<svg>` element or embedded in an `<img>` element using the Base64 format.

[Graphviz]: https://www.graphviz.org


Installation
------------

This plugin can be installed via:

    python -m pip install pelican-graphviz

The newly installed plugin should be detected and enabled automatically, unless the `PLUGINS` variable is used in the Pelican settings file. In this case, `"graphviz"` must be added to the existing `PLUGINS` list. Further information can be found in the [How to Use Plugins](https://docs.getpelican.com/en/latest/plugins.html#how-to-use-plugins) documentation.

This plugin will be deactivated if Graphviz is not installed on the system. On Debian-based systems, Graphviz can be installed via:

    sudo aptitude install graphviz

For macOS, Graphviz can be installed via Homebrew:

    brew install graphviz


Usage
-----

### Markdown

In the Markdown source, the Graphviz code should be inserted as a separate block, i.e. with blank lines separating it from the surrounding text. An example is shown below:

```markdown
..graphviz dot
digraph G {
  graph [rankdir = LR];
  Hello -> World
}
```

This will insert an image into your article, as shown here:

![figure](https://github.com/pelican-plugins/graphviz/raw/main/hello-world.png)

The block must start with `..graphviz` (this is configurable — see below). The word `dot` in the first line indicates which program will be used to produce the image. The available programs are: `dot`, `neato`, `twopi`, `circo`, `fdp`, `sfdp`, and `patchwork` (see the [Graphviz documentation][] for details). The Graphviz code must start on the second line of the block. Please note that *newlines are not allowed inside the Graphviz block*.

[Graphviz documentation]: https://www.graphviz.org/documentation/

### reStructuredText

For RST input, support is implemented as a directive, with syntax like:

```rst
.. graphviz:: dot
   :alt-text: My graph

   digraph G {
     graph [rankdir = LR];
     Hello -> World
   }
```

Styling with CSS
----------------

The image is generated in HTML using an `<img>` element inside an HTML element (by default a `<div>`, but this can be configured — see below). The latter has the class `graphviz` (this is also configurable — see below). One possible CSS styling would be:

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

The following variables can be configured in the Pelican settings file:

- `GRAPHVIZ_BLOCK_START`: Starting tag for the Graphviz block in Markdown (defaults to `'..graphviz'`). This setting has no effect for reStructuredText input.

- `GRAPHVIZ_HTML_ELEMENT`: The HTML element inside which the generated Graphviz image is inserted (defaults to `'div'`; another sensible option would be `'span'`).

- `GRAPHVIZ_IMAGE_CLASS`: The class of the `<div>` element containing the generated Graphviz image (defaults to `'graphviz'`).

- `GRAPHVIZ_COMPRESS`: Compress the resulting SVG XML to an image (defaults to `True`). Without compression, more SVG features are available, for instance the inclusion of clickable URLs inside the Graphviz diagram.

- `GRAPHVIZ_ALT_TEXT`: The string that will be used as the default value for the `alt` property of the generated `<img>` HTML element (defaults to `"[GRAPH]"`). It is only meaningful when the resulting SVG output is compressed.

The values for all variables above, except `GRAPHVIZ_BLOCK_START`, can be overridden for each block individually using the following syntax in Markdown:

```markdown
..graphviz [key1=val1, key2="val2"...] dot
```
If the value includes a comma (`,`) or an equal sign (`=`), then use the `key2="val2"` form.

Or in reStructuredText:

```rst
.. graphviz:: dot
   :key1: val1
   :key2: val2
```

The allowed keys are `html-element`, `image-class`, `alt-text`, and `compress`. For the latter, the value can be either `yes` or `no`.

Output Image Format
-------------------

The embedded image is in SVG format, and cannot currently be changed. This format was chosen over others, such as PNG, for two reasons. First, the generated Base64 `src` string is usually shorter shorter for SVG than for PNG. Second, the image will be available in a high-quality vectorized format when displayed in the browser. However, note that this choice may prevent display in browsers lacking proper SVG support.


Text alternative for the image
------------------------------

When generating compressed SVG images (the default), an `<img>` element will appear in the HTML output. According to the [Web Content Accessibility Guidelines], non-text content, such as `<img>` elements, should have an text alternative. The graphviz plugin complies with this recommendation and always generate an `alt` property for the generated `<img>` element. The value of the `alt` property will be, in order of priority:

1. The value of the Graphviz block option `alt-text`,
2. the ID of the Graphviz element (`"G"` in the example above), or
3. the value of the global configuration variable `GRAPHVIZ_ALT_TEXT`.

[Web Content Accessibility Guidelines]: https://www.w3.org/TR/WCAG22/#non-text-content


Alternatives
------------

An alternative to this plugin is the [Graphviz tag][] provided by the [Liquid Tags plugin][], which differs from this plugin in several respects. First, the Liquid Tags version uses the syntax `{% graphviz { <program> […] } %}`, while the graphviz plugin uses the Markdown extension syntax `..graphviz <program> […]`. The differences in the rendered output are:

- Both plugins output an element with the attribute `class="graphviz"`. However, only the graphviz plugin allows you to change the class name via a configuration variable (`GRAPHVIZ_IMAGE_CLASS`).
- Liquid Tags encodes the image as `src="data:image/png;base64,[…]"`, whereas the graphviz plugin encodes it as `src="data:image/svg+xml;base64,[…]"`. This has two impacts. First, the size of the HTML code produced by the graphviz plugin is much smaller. For example, the Base64 string for the graphviz code `digraph graphname {a -> b -> c; b -> d;}` is four times smaller. Second, the Liquid Tags version generates a raster image file, whereas the graphviz plugin produces a vector image that can be zoomed in on without losing image quality.
- Liquid Tags outputs the Graphviz image inside a `<span>`, whereas the graphviz plugin offers a choice for the container element.

[Graphviz tag]: https://github.com/pelican-plugins/liquid-tags/blob/main/pelican/plugins/liquid_tags/graphviz.py
[Liquid Tags plugin]: https://github.com/pelican-plugins/liquid-tags


Contributing
------------

Contributions are welcome and greatly appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].

To start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.

[existing issues]: https://github.com/pelican-plugins/graphviz/issues
[Contributing to Pelican]: https://docs.getpelican.com/en/latest/contribute.html


Acknowledgments
---------------

Thanks to [Justin Mayer][], for helping with migration of this plugin under the Pelican Plugins organization, and to [Maxim Kochurov][], for introducing the `GRAPHVIZ_COMPRESS` configuration variable.

[Justin Mayer]: https://github.com/justinmayer
[Maxim Kochurov]: https://github.com/ferrine

Thanks to [weeheavy] for suggesting the addition of the `alt` property to the HTML `<img>` generated element (issue [#30]).

[weeheavy]: https://github.com/weeheavy
[#30]: https://github.com/pelican-plugins/graphviz/issues/30

Thanks to [Mark Shroyer][] for fixing lint issues, re-enabling the unit test `TestGraphvizAltTextWithoutID` (PR [#31]) and adding reStructuredText supoort (PRs [#34] and [#35]) 

[Mark Shroyer]: https://github.com/mshroyer
[#31]: https://github.com/pelican-plugins/graphviz/pull/31
[#34]: https://github.com/pelican-plugins/graphviz/pull/34
[#35]: https://github.com/pelican-plugins/graphviz/pull/35


Authors
-------

Copyright © 2015, 2021, 2023–2026  Rafael Laboissière <rafael@laboissiere.net>

Copyright © 2025  Mark Shroyer <mark@shroyer.name>


License
-------

This project is licensed under the terms of the AGPL license, version 3.0 or later.
