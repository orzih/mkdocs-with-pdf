# Sample with `Mkdocs document`

- [Output PDF](document.pdf)

## Test source

|            |                                               |
| ---------- | --------------------------------------------- |
| Repository | https://github.com/squidfunk/mkdocs-material/ |
| Commit     | 889a9f03d42cbe3cbbbe393d6098eb92a3fc6bb3      |

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

```sh
$ mkdocs build
INFO    -  Cleaning site directory
INFO    -  Building documentation to directory: /tmp/mkdocs-with-pdf/samples/mkdocs-material/site
WARNING -  Missing article: [Home]()
INFO    -  Number headings up to level 3.
INFO    -  Generate a table of contents up to heading level 3.
INFO    -  Generate a cover page.
ERROR   -  No anchor #.: for internal URI reference
INFO    -  Converting 34 articles to PDF took 19.3s
INFO    -  Documentation built in 22.46 seconds
```
