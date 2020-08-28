# Sample with `Mkdocs document`

- [Output PDF](document.pdf)

## Test source

|            |                                               |
| ---------- | --------------------------------------------- |
| Repository | https://github.com/squidfunk/mkdocs-material/ |
| Commit     | c6c67608853f539e97f2fae5ff137fa394d66813      |

- use Original
  - .browserslistrc
  - CONTRIBUTING.md
  - LICENSE
  - docs/ - (with fix broken links)
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
INFO    -  Converting 34 articles to PDF took 25.1s
INFO    -  Documentation built in 28.22 seconds
```
