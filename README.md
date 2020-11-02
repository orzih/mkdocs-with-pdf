# PDF Generate Plugin for MkDocs

[![PyPI version](https://img.shields.io/pypi/v/mkdocs-with-pdf.svg)](https://pypi.org/project/mkdocs-with-pdf)
[![PyPI downloads](https://img.shields.io/pypi/dm/mkdocs-with-pdf.svg)](https://pypi.org/project/mkdocs-with-pdf)

---

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
1. Python 3.5 or higher
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
        #back_cover: true
        #cover_title: TITLE TEXT
        #cover_subtitle: SUBTITLE TEXT
        #custom_template_path: TEMPLATES PATH
        #
        #toc_title: TOC TITLE TEXT
        #heading_shift: false
        #toc_level: 3
        #ordered_chapter_level: 2
        #excludes_children:
        #    - 'release-notes/:upgrading'
        #    - 'release-notes/:changelog'
        #
        #exclude_pages:
        #    - 'bugs/'
        #    - 'appendix/contribute/'
        #convert_iframe:
        #    - src: IFRAME SRC
        #      img: POSTER IMAGE URL
        #      text: ALTERNATE TEXT
        #    - src: ...
        #two_columns_level: 3
        #
        #render_js: true
        #headless_chrome_path: headless-chromium
        #
        #output_path: any-place/document.pdf
        #enabled_if_env: ENABLE_PDF_EXPORT
        #
        #debug_html: true
        #show_anchors: true
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

* `back_cover`

    Set the value to `true` if you need a back cover page.  
    **default**: `false`  
    _**since**: `v0.8.0`_

    You would be better to install the `qrcode` package:

    ```sh
    pip install qrcode
    ```

* `cover_title`

    Set the title text in cover page.  
    **default**: use `site_name` in your project `mkdocs.yml`

* `cover_subtitle`

    Set the subtitle text in cover page.  
    **default**: `None`

* `cover_logo`

    Set the logo image in cover page. This value is URL or simply specify the relative path to the docs directory.  
    **default**: `None`  
    _**since**: `v0.8.0`_

##### for Heading and TOC

* `toc_title`

    Set the title text of _Table of Content_.  
    **default**: `Table of Content`  
    _**since**: `v0.4.0`_

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

* `convert_iframe`

    List of `iframe` to `a` conversions. Every `iframe` that matches a `src` in this list will be replace to `a` contains each `img` and/or `text`. it's using for such as embedded VIDEO.  
    **default**: `[]`  
    _**since**: `v0.6.0`_

    @see [Sample of _MkDocs Material_](https://github.com/orzih/mkdocs-with-pdf/blob/master/samples/mkdocs-material/)

* `two_columns_level` (Experimental)

    Set the heading level of **_Two Column Layout_**. Currently only `0`(disable) or `3` is valid for this value. So slow processing, but a little nice.  

    **default**: `0`  
    _**since**: `v0.7.0`_

    @see [Sample of _MkDocs Material_](https://github.com/orzih/mkdocs-with-pdf/blob/master/samples/mkdocs-material/)

##### Renderer for JavaScript

* `render_js`

    Set the value to `true` if you're using '[MathJax](https://www.mathjax.org/)', '[Twemoji](https://twemoji.twitter.com/)' or any more.  
    Require "Chrome" which has "headless" mode.  

    **default**: `false`  
    _**since**: `v0.7.0`_

* `headless_chrome_path`

    Set the "Headless Chrome" program path.  
    If `render_js` is _`false`_, this value will be ignored.  

    **default**: `chromium-browser`

> Check on your system:
>
> ```
> $ <PROGRAM_PATH> --headless \
>    --disable-gpu \
>    --dump-dom \
>    <ANY_SITE_URL(eg. 'https://google.com')>
> ```

##### ... and more

* `output_path`

    This option allows you to use a different destination for the PDF file.  
    **default**: `pdf/document.pdf`

* `custom_template_path`

    The path where your custom `cover.html` and/or `styles.scss` are located.
    **default**: `templates`  
    _**since**: `v0.8.0`_

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

* `show_anchors`

    Setting this to `true` will list out of anchor points provided during the build as info message.  
    **default**: `false`  
    _**since**: `v0.7.4`_

* `verbose`

    Setting this to `true` will show all WeasyPrint debug messages during the build.  
    **default**: `false`

## Custom cover page and document style

It is possible to create a custom cover page for the document.
You can also add a custom style sheet to modify the whole document.

To do so, add a `templates` folder at the root level of your `mkdocs` project and place a `cover.html` and/or a `styles.scss` inside.
Alternatively, you can specify a different location with the `custom_template_path` option.

### Custom cover page

Using [jinja2](https://jinja.palletsprojects.com/en/2.11.x/templates/) syntax, you can access all data from your `mkdocs.yml`.
To make template creation easier, you can use `plugin_some_plugin` to access variables from plugins.
E.g. use `{{ author }}` to get the author from your `mkdocs.yml` that looks like:

```yaml
plugins:
    - with-pdf:
        author: WHO
```

You can use custom variables [`extra:` in your `mkdocs.yml`](https://www.mkdocs.org/user-guide/configuration/#extra)
And, you can check it in the log if run with `verbose` or `debug_html` options.

### Custom stylesheet

Since your stylesheet is appended to the default ones, you can override every setting from them.

Tip: setting the `debug_html` option to `true` to get the generated html that is passed to `weasyprint` can help you determine the html tags, classes or identifiers you want to modify in your stylesheet.

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
