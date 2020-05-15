# Sample with `Mkdocs document`

- [Output PDF](document.pdf)

## Test source

|            |                                               |
| ---------- | --------------------------------------------- |
| Repository | https://github.com/mkdocs/mkdocs/             |
| Commit     | ff0b7260564e65b6547fd41753ec971e4237823b      |

- use Original
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
ERROR   -  No anchor #user-guide/plugins/:plugins for internal URI reference
ERROR   -  No anchor #user-guide/writing-your-docs/:index_pages for internal URI reference
ERROR   -  No anchor #user-guide/deploying-your-docs/:readthedocs for internal URI reference
ERROR   -  No anchor #user-guide/styling-your-docs/:using-the-theme_dir for internal URI reference
ERROR   -  No anchor #user-guide/plugins/:plugins for internal URI reference
ERROR   -  No anchor #user-guide/custom-themes/:search_and_themes for internal URI reference
ERROR   -  No anchor #user-guide/plugins/:plugins for internal URI reference
ERROR   -  No anchor #user-guide/writing-your-docs/:multilevel-documentation for internal URI reference
ERROR   -  No anchor #user-guide/styling-your-docs/:search-and-themes for internal URI reference
ERROR   -  No anchor #user-guide/styling-your-docs/:global-context for internal URI reference
INFO    -  Converting 10 articles to PDF took 7.2s
INFO    -  Documentation built in 7.63 seconds
```
