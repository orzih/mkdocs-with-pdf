# Sample with `Mkdocs document`

- [Output PDF](document.pdf)

## Test source

|            |                                               |
| ---------- | --------------------------------------------- |
| Repository | https://github.com/squidfunk/mkdocs-material/ |
| Commit     | a43679b1048c39c21861e4c622e2e3f2c6cdc90b      |

- use Original
  - CONTRIBUTING.md
  - docs/
  - material/
- modified
  - mkdocs.yml - modified
- added
  - docs/assets/css

```sh
$ mkdocs build
INFO    -  Cleaning site directory
INFO    -  Building documentation to directory: /tmp/mkdocs-with-pdf/samples/mkdocs-material/site 
INFO    -  Number headings up to level 3.
INFO    -  Generate a table of contents up to heading level 3.
INFO    -  Generate a cover page.
ERROR   -  No anchor #extensions/pymdown/:pymdown for internal URI reference
ERROR   -  No anchor #plugins/getting-started.md/:language for internal URI reference
ERROR   -  No anchor #plugins/getting-started.md/:language for internal URI reference
INFO    -  Converting 19 articles to PDF took 17.1s
INFO    -  Documentation built in 18.98 seconds
```
