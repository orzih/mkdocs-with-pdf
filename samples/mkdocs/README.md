# Sample with `Mkdocs document`

- [Output PDF](document.pdf)

## Test source

|            |                                               |
| ---------- | --------------------------------------------- |
| Repository | https://github.com/mkdocs/mkdocs/             |
| Commit     | ff0b7260564e65b6547fd41753ec971e4237823b      |

- use Original (with fix broken links)
  - docs/
- modified
  - mkdocs.yml - modified
- added
  - docs/css/pdf-print.css

### build log

```sh
$ mkdocs build
INFO    -  Cleaning site directory
INFO    -  Building documentation to directory: /tmp/mkdocs-with-pdf/samples/mkdocs/site
INFO    -  Number headings up to level 3.
INFO    -  Generate a table of contents up to heading level 2.
INFO    -  Generate a cover page.
INFO    -  Converting 10 articles to PDF took 7.3s
INFO    -  Documentation built in 7.75 seconds
```
