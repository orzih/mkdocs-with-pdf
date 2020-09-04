# Sample with `Mkdocs document`

- [Output PDF](document.pdf)

## Test source

|            |                                               |
| ---------: | --------------------------------------------- |
| Repository | https://github.com/squidfunk/mkdocs-material/ |
| Commit     | 9b88f712ba278cb35dd345d1b43fd11da36374c1      |

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

```none
$ mkdocs build
INFO    -  Cleaning site directory
INFO    -  Building documentation to directory: /tmp/mkdocs-with-pdf/samples/mkdocs-material/site
WARNING -  Missing article: [Home]()
INFO    -  Number headings up to level 3.
INFO    -  Generate a table of contents up to heading level 2.
INFO    -  Generate a cover page.
ERROR   -  No anchor #.: for internal URI reference
INFO    -  Converting 35 articles to PDF took 25.3s
INFO    -  Documentation built in 28.48 seconds
```

## TODO

- [ ] `Hero page` conversion.
- [ ] `twemoji` polyfill.
- [ ] `MathJax` supports (with rendering with JS).
- [ ] ... and something.
