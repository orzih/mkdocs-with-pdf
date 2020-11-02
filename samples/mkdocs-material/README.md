# Sample with `Mkdocs document`

- [Output PDF](document.pdf)

## Test source

|            |                                               |
| ---------: | --------------------------------------------- |
| Repository | https://github.com/squidfunk/mkdocs-material/ |
| Commit     | 81944ae1a1c3de0b37691c6dc3a0bc70fe4980b9      |

- use Original
  - .browserslistrc
  - CONTRIBUTING.md
  - LICENSE
  - docs/
  - material/
- modified
  - mkdocs.yml - modified
- added
  - docs/assets/css

```console
$ mkdocs build
INFO    -  Cleaning site directory
INFO    -  Building documentation to directory: /tmp/mkdocs-with-pdf/samples/mkdocs-material/site
WARNING -  Missing article: [Home]()
INFO    -  Number headings up to level 3.
INFO    -  Generate a table of contents up to heading level 2.
INFO    -  Generate a cover page with "default_cover.html.j2".
INFO    -  Generate a back cover page with "default_back_cover.html.j2".
INFO    -  Converting <img> alignment(workaround).
INFO    -  Converting <iframe> to poster image(if available).
INFO    -  Converting for two-column layout(heading level 3).
INFO    -  Rendering on `Headless Chrome`(execute JS).
INFO    -  Rendering for PDF.
INFO    -  Output a PDF to "/tmp/mkdocs-with-pdf/samples/mkdocs-material/site/../document.pdf".
ERROR   -  No anchor #.: for internal URI reference
INFO    -  Converting 38 articles to PDF took 272.3s
INFO    -  Documentation built in 275.89 seconds
```

## TODO

- [ ] `Hero page` conversion.
- [ ] `twemoji` polyfill.
- [ ] `MathJax` supports (with rendering with JS).
- [ ] ... and something.
