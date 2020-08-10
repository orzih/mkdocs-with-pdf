import unittest

import os
from weasyprint import urls
from mkdocs_with_pdf.preprocessor.links.transform import transform_href


class TransformHrefTestCase(unittest.TestCase):

    def test_transform_href(self):

        patterns = [
            # [[href, rel_url], x_href]

            [['./', '.'], '#.:'],
            [['#hash', '.'], '#.:hash'],

            [['./', 'path/'], '#path/:'],
            [['#hash', 'path/'], '#path/:hash'],
            [['#hash:1', 'path/'], '#path/:hash:1'],
            [['target/', 'path/'], '#path/target/:'],
            [['target/#hash', 'path/'], '#path/target/:hash'],
            [['../', 'path/'], '#./:'],
            [['../#hash', 'path/'], '#/:hash'],
            [['../target/', 'path/'], '#target/:'],
            [['../target/#hash', 'path/'], '#target/:hash'],

            [['./', 'path/sub/'], '#path/sub/:'],
            [['#hash', 'path/sub/'], '#path/sub/:hash'],
            [['target/', 'path/sub/'], '#path/sub/target/:'],
            [['target/#hash', 'path/sub/'], '#path/sub/target/:hash'],
            [['../', 'path/sub/'], '#path/:'],
            [['../#hash', 'path/sub/'], '#path/:hash'],
            [['../target/', 'path/sub/'], '#path/target/:'],
            [['../target/#hash', 'path/sub/'], '#path/target/:hash'],
            [['../../', 'path/sub/'], '#.:'],
            [['../../#hash', 'path/sub/'], '#.:hash'],
            [['../../target/', 'path/sub/'], '#target/:'],
            [['../../target/#hash', 'path/sub/'], '#target/:hash'],


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
            [['../index.html', 'another/index.html'], '#another/index.html:'],
            [['#hash', 'path1/index.html'], '#path1/index:hash'],
            [['#hash', 'path2/index.html'], '#path2/index:hash'],
            [['#hash', 'path3/index.html'], '#path3/index:hash'],

            # Internal links with `use_directory_urls: false`
            [['#one', 'test.html'], '#test:one'],
            [['#one', 'test2.html'], '#test2:one'],
            [['test2.html#one', 'test.html'], '#test2:one'],
            [['#one', 'path/test.html'], '#path/test:one'],
            [['#one', 'path/sub/test.html'], '#path/sub/test:one'],

            [['target/test.html', 'path/c.html'], '#path/target/test:'],
            [['target/test.html#hash', 'path/c.html'], '#path/target/test:hash'],
            [['../target/test.html', 'path/c.html'], '#target/test:'],
            [['../target/test.html#hash', 'path/c.html'], '#target/test:hash'],

            [['target/test.html', 'path/sub/c.html'], '#path/sub/target/test:'],
            [['target/test.html#hash', 'path/sub/c.html'], '#path/sub/target/test:hash'],
            [['../target/test.html', 'path/sub/c.html'], '#path/target/test:'],
            [['../target/test.html#hash', 'path/sub/c.html'], '#path/target/test:hash'],
            [['../../target/test.html', 'path/sub/c.html'], '#target/test:'],
            [['../../target/test.html#hash', 'path/sub/c.html'], '#target/test:hash'],

            [['//example.com/test.html', 'any/index.html'], '//example.com/test.html'],
            [['https://example.com/test.html', 'any/index.html'], 'https://example.com/test.html'],
            [['https://example.com/test.html#frag', 'any/index.html'], 'https://example.com/test.html#frag'],
            [['mailto:example.com/test.html', 'any/index.html'], 'mailto:example.com/test.html'],

            [['../', '.'], '#'],
            [['../', 'index.html'], '#'],
            [['../index.html', 'index.html'], '#'],
            [['../index.html#hash', 'index.html'], '#'],

            [['../../', 'path/'], '#'],
            [['../../', 'path/index.html'], '#'],
            [['../../index.html', 'path/'], '#'],
            [['../../index.html', 'path/index.html'], '#'],
            [['../../index.html#hash', 'path/index.html'], '#'],

            [['../../../', 'path/sub/'], '#'],
            [['../../../', 'path/sub/index.html'], '#'],
            [['../../../index.html', 'path/sub/'], '#'],
            [['../../../index.html', 'path/sub/index.html'], '#'],
            [['../../../index.html#hash', 'path/sub/index.html'], '#'],
            [['../../../index.html', 'path/sub.html'], '#'],
            [['../../../index.html', 'path/sub.html'], '#'],
            [['../../../index.html#hash', 'path/sub.html'], '#'],

        ]

        for pattern in patterns:
            with self.subTest(pattern=pattern):
                case, x_href = pattern
                href, rel_url = case

                if urls.url_is_absolute(href) or os.path.isabs(href):
                    self.assertTrue(True)
                    continue

                r = transform_href(href, rel_url)
                self.assertEqual(r, x_href)
