CHANGELOG
=========

1.3.0 - 2025-01-18
------------------

The `<img>` element containing the compressed SVG figure will always have an text alternative (`alt` property). This text can be specified using the `alt-text` option of the graphviz block 
(fixes issue #30)

1.2.5 - 2024-04-14
------------------

Ensure plugin is included in sdist build

1.2.4 - 2024-04-07
------------------

Maintainance release (no user visible changes)

* Add Python 3.12 to CI test matrix
* Switch build system from Hatchling to PDM
* Fix linter configuration

1.2.3 - 2023-10-31
------------------

Maintenance release:

- Migrate to the new tooling standards
- Improve code quality

1.2.2 - 2021-11-04
------------------

Maintenance release:
- Add Acknowledgments section in documentation
- Use full URL for the figure in the documentation

1.2.1 - 2021-11-04
------------------

Maintenance release:

- Drop item in ToDo list (was implemented in the previous release)

- Use .format() instead of % operator to format strings

- Add unit test for the setting of per-block configuration options

1.2.0 - 2021-11-03
------------------

Allow per-block configuration settings

1.1.0 - 2021-11-01
------------------

Allow the SVG XML output code to be uncompressed (through the new
configuration variable GRAPHVIZ_COMPRESS). This allows more featureful
SVG images, for instance including clickable URLs. Thanks to Maxim
Kochurov for the contribution.

1.0.1 - 2021-05-03
------------------

Fix initialization of error flag variable (concerns OS name "nt")

1.0.0 - 2021-04-05
------------------

Initial release as namespace plugin
