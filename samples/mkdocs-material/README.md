# Sample with `Mkdocs document`

- [Output PDF](document.pdf)

## Test source

|            |                                               |
| ---------: | --------------------------------------------- |
| Repository | https://github.com/squidfunk/mkdocs-material/ |
| Commit     | f9f48c09c1e33c64cab27250f597e84906c300d5      |

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
INFO    -  Generate a cover page.
INFO    -  Converting <img> alignment(workaround).
INFO    -  Converting <iframe> to poster image(if available).
INFO    -  Converting for two-column layout(heading level 3).
INFO    -  Rendering on `Headless Chrome`(execute JS).
INFO    -  Rendering for PDF.
INFO    -  Output a PDF to "/tmp/mkdocs-with-pdf/samples/mkdocs-material/site/../document.pdf".
ERROR   -  No anchor #.: for internal URI reference
INFO    -  Converting 37 articles to PDF took 268.5s
INFO    -  Documentation built in 271.76 seconds
```

## TODO

- [ ] `Hero page` conversion.
- [ ] `twemoji` polyfill.
- [ ] `MathJax` supports (with rendering with JS).
- [ ] ... and something.
