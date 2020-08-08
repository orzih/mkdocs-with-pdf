import unittest

from mkdocs_with_pdf.preprocessor.links.transform import transform_href


class TransformHrefTestCase(unittest.TestCase):

    def test_transform_href(self):

        patterns = [
            # [[href, rel_url], x_href]

            [['.', '.'], '#.:'],
            [['./', 'path/'], './'],
            [['./', 'path/sub/'], './'],

            [['..', 'path/'], '#/:'],
            [['../#hash', 'path/'], '#/:hash'],
            [['../../#hash', 'path/sub/'], '#/:hash'],

            [['../../target/', 'path/'], '../../target/'],
            [['../../target/#hash', 'path/'], '#target/:hash'],
            [['../../target/', 'path/sub/'], '../../target/'],
            [['../../target/#hash', 'path/sub/'], '#target/:hash'],

            [['#hash', 'path/'], '#path/:hash'],
            [['#hash', 'path/sub/'], '#path/sub/:hash'],
            [['#hash:1', 'path/'], '#path/:hash:1'],

            # what is this?
            [['../page.md/#hash', 'path/sub/'], '#page/:hash'],

            [['page.html', 'index.html'], '#page.html:'],
            [['page.html#hash', 'index.html'], '#page:hash'],
            [['page.html', 'other.html'], '#page.html:'],

            # 'index' links
            [['index.html', 'path1/index.html'], '#path1/index.html:'],
            [['index.html', 'path2/index.html'], '#path2/index.html:'],
            [['path1/index.html', 'index.html'], '#path1/index.html:'],
            [['path2/index.html', 'index.html'], '#path2/index.html:'],
            [['../path1/index.html', 'another/index.html'], '#path1/index.html:'],
            [['../path2/index.html', 'another/index.html'], '#path2/index.html:'],
            [['#hash', 'path1/index.html'], '#path1/index:hash'],
            [['#hash', 'path2/index.html'], '#path2/index:hash'],
            [['#hash', 'path3/index.html'], '#path3/index:hash'],

            # Internal links with `use_directory_urls: false`
            [['#one', 'test.html'], '#test:one'],
            [['#one', 'test2.html'], '#test2:one'],
            [['test2.html#one', 'test.html'], '#test2:one'],
            [['#one', 'path/test.html'], '#path/test:one'],
            [['#one', 'path/sub/test.html'], '#path/sub/test:one'],

        ]

        for pattern in patterns:
            with self.subTest(pattern=pattern):
                case, x_href = pattern
                href, rel_url = case

                r = transform_href(href, rel_url)
                self.assertEqual(r, x_href)
