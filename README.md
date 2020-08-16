# PDF Generate Plugin for MkDocs

[![PyPI version](https://img.shields.io/pypi/v/mkdocs-with-pdf.svg)](https://pypi.org/project/mkdocs-with-pdf)

This plugin will generate a single PDF file from your MkDocs repository.
This plugin is inspired by [MkDocs PDF Export Plugin][mkdocs-pdf-export-plugin].

## Features

* Cover and Table of Contents integrated in the PDF
* Automatically numbers on heading(h1-h3).
* Shift down sub-page headings level.
* using [WeasyPrint][weasyprint].

## Samples

* [PDF of _'MkDocs' docs_][sample_mkdocs]
* [PDF of _'Material for MkDocs' docs_][sample_mkdocs-material]

[sample_mkdocs]: https://github.com/orzih/mkdocs-with-pdf/blob/master/samples/mkdocs/README.md
[sample_mkdocs-material]: https://github.com/orzih/mkdocs-with-pdf/blob/master/samples/mkdocs-material/README.md

## Requirements

1. This package requires MkDocs version 1.0 or higher (0.17 works as well)
1. Python 3.4 or higher
1. WeasyPrint depends on cairo, Pango and GDK-PixBuf which need to be installed separately. Please follow the installation instructions for your platform carefully:
    * [Linux][weasyprint-linux]
    * [MacOS][weasyprint-macos]
    * [Windows][weasyprint-windows]

## How to use

### Installation

1. Install the package with pip:

    ```bash
    pip install mkdocs-with-pdf
    ```

2. Enable the plugin in your `mkdocs.yml`:

    ```yaml
    plugins:
        - with-pdf
    ```

    More information about plugins in the [MkDocs documentation][mkdocs-plugins].

#### Testing

When building your repository with `mkdocs build`, you should now see the following message at the end of your build output:

> Converting 10 articles to PDF took 7.1s

### Configuration

You may customize the plugin by passing options in `mkdocs.yml`:

```yaml
plugins:
    - with-pdf:
        #author: WHO
        #copyright: ANY TEXT
        #
        #cover: false
        #cover_title: TITLE TEXT
        #cover_subtitle: SUBTITLE TEXT
        #heading_shift: false
        #toc_level: 3
        #ordered_chapter_level: 2
        #excludes_children:
        #    - 'release-notes/:upgrading'
        #    - 'release-notes/:changelog'
        #exclude_pages:
        #    - 'bugs/'
        #    - 'appendix/contribute/'
        #output_path: any-place/document.pdf
        #enabled_if_env: ENABLE_PDF_EXPORT
        #
        #debug_html: true
        #verbose: true
```

#### Options

##### for Properties

* `author`

    Set the author text.  
    **default**: use `site_author` in your project `mkdocs.yml`

* `copyright`

    Set the author text.  
    **default**: use `copyright` in your project `mkdocs.yml`

> `author` and `copyright` values are drawn in Cover, and you can use '@page' content.  
>
> ```css "e.g."
> @page {
>   @bottom-left {
>     content: string(author) !important;
>   }
>   @bottom-right {
>     content: string(copyright) !important;
>   }
> }
> ```

##### for Cover

* `cover`

    Set the value to `false` if you don't need a cover page.  
    **default**: `true`

* `cover_title`

    Set the title text in cover page.  
    **default**: use `site_name` in your project `mkdocs.yml`

* `cover_subtitle`

    Set the subtitle text in cover page.  
    **default**: `None`

##### for Heading and TOC

* `toc_title`

    Set the title text of _Table of Content_.  
    **default**: `Table of Content`

* `heading_shift`

    Set this value to `false`, disable shift heading in child page.  
    **default**: `true`

    In this flags enable, heading move down one level in child page.

* `toc_level`

    Set the level of _Table of Content_. This value is enabled in the range of from `1` to `3`.  
    **default**: `3`

* `ordered_chapter_level`

    Set the level of heading number addition. This value is enabled in the range of from `1` to `3`.  
    **default**: `3`

* `excludes_children`

    Set the page `id` of `nav` url. If the `id` matches in this list, it will be excluded from the heading number addition and table of contents.  
    **default**: `[]`

##### for Page

* `exclude_pages`

    Set the page `id` of `nav` url. If the `id` matches in this list, it will be excluded page contents.  
    **default**: `[]`  
    _**since**: `v0.3.0`_

##### ... and more

* `output_path`

    This option allows you to use a different destination for the PDF file.  
    **default**: `pdf/document.pdf`

* `enabled_if_env`

    Setting this option will enable the build only if there is an environment variable set to 1. This is useful to disable building the PDF files during development, since it can take a long time to export all files.  
    **default**: `None`

* `debug_html`

    Setting this to `true` will out HTML to `stdout` on build time.  
    **default**: `false`

    You can try this:

    ```bash
    mkdocs build > for_pdf_print.html
    ```

* `verbose`

    Setting this to `true` will show all WeasyPrint debug messages during the build.  
    **default**: `false`

## Contributing

From reporting a bug to submitting a pull request: every contribution is appreciated and welcome. Report bugs, ask questions and request features using [Github issues][github-issues].
If you want to contribute to the code of this project, please read the [Contribution Guidelines][contributing].

## Special thanks to

* [Terry Zhao][zhaoterryy] the author of the [MkDocs PDF Export Plugin][mkdocs-pdf-export-plugin] the source of our inspiration. We've used some of his code in this project.

[mkdocs-pdf-export-plugin]: https://github.com/zhaoterryy/mkdocs-pdf-export-plugin
[zhaoterryy]:  https://github.com/zhaoterryy

[weasyprint]: http://weasyprint.org/
[weasyprint-linux]: https://weasyprint.readthedocs.io/en/latest/install.html#linux
[weasyprint-macos]: https://weasyprint.readthedocs.io/en/latest/install.html#os-x
[weasyprint-windows]: https://weasyprint.readthedocs.io/en/latest/install.html#windows

[mkdocs-plugins]: http://www.mkdocs.org/user-guide/plugins/
[mkdocs-material]: https://github.com/squidfunk/mkdocs-material

[contributing]: https://github.com/orzih/mkdocs-with-pdf/blob/master/CONTRIBUTING.md
[github-issues]: https://github.com/orzih/mkdocs-with-pdf/issues
