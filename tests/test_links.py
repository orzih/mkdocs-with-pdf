import unittest

import os
from weasyprint import urls
from mkdocs_with_pdf.preprocessor.links.transform import transform_href


class TransformHrefTestCase(unittest.TestCase):

    def test_transform_href(self):

        def run_test(scene: str, patterns: []):
            for index, pattern in enumerate(patterns):
                with self.subTest(index=index, pattern=pattern):
                    case, x_href = pattern
                    href, rel_url = case

                    # check on `preprocessor.get_combined`
                    if urls.url_is_absolute(href) or os.path.isabs(href):
                        self.assertTrue(True)
                        continue

                    r = transform_href(href, rel_url)
                    self.assertEqual(r, x_href, f'"{scene}" at {index}')

        run_test('on TOP(level 0)', [
            # [[href, rel_url], x_href]
            [['./', '.'], '#.:'],
            [['#hash', '.'], '#.:hash'],
        ])

        run_test('on Subpath(level 1)', [
            # [[href, rel_url], x_href]
            [['./', 'path/'], '#path/:'],
            [['#hash', 'path/'], '#path/:hash'],
            [['#hash:1', 'path/'], '#path/:hash:1'],
            [['target/', 'path/'], '#path/target/:'],
            [['target/#hash', 'path/'], '#path/target/:hash'],
            [['../', 'path/'], '#.:'],
            [['../#hash', 'path/'], '#.:hash'],
            [['../target/', 'path/'], '#target/:'],
            [['../target/#hash', 'path/'], '#target/:hash'],
        ])

        run_test('on Subpath(level 2)', [
            # [[href, rel_url], x_href]
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
        ])

        run_test('on Subpath(level 3)', [
            # [[href, rel_url], x_href]
            [['./', 'p0/p1/p2/'], '#p0/p1/p2/:'],
            [['#h', 'p0/p1/p2/'], '#p0/p1/p2/:h'],
            [['target/', 'p0/p1/p2/'], '#p0/p1/p2/target/:'],
            [['target/#h', 'p0/p1/p2/'], '#p0/p1/p2/target/:h'],
            [['../', 'p0/p1/p2/'], '#p0/p1/:'],
            [['../#h', 'p0/p1/p2/'], '#p0/p1/:h'],
            [['../target/', 'p0/p1/p2/'], '#p0/p1/target/:'],
            [['../target/#h', 'p0/p1/p2/'], '#p0/p1/target/:h'],
            [['../../', 'p0/p1/p2/'], '#p0/:'],
            [['../../#h', 'p0/p1/p2/'], '#p0/:h'],
            [['../../target/', 'p0/p1/p2/'], '#p0/target/:'],
            [['../../target/#h', 'p0/p1/p2/'], '#p0/target/:h'],
            [['../../../', 'p0/p1/p2/'], '#.:'],
            [['../../../#h', 'p0/p1/p2/'], '#.:h'],
            [['../../../target/', 'p0/p1/p2/'], '#target/:'],
            [['../../../target/#h', 'p0/p1/p2/'], '#target/:h'],
        ])

        run_test('on root(level 0) - use_directory_urls: false', [
            # [[href, rel_url], x_href]
            [['page.html', 'index.html'], '#page/:'],
            [['page.html#hash', 'index.html'], '#page/:hash'],
            [['page.html', 'other.html'], '#page/:'],
        ])

        run_test('"index" links', [
            # [[href, rel_url], x_href]
            [['index.html', 'path1/index.html'], '#path1/:'],
            [['index.html', 'path2/index.html'], '#path2/:'],
            [['path1/index.html', 'index.html'], '#path1/:'],
            [['path2/index.html', 'index.html'], '#path2/:'],
            [['../path1/index.html', 'another/index.html'], '#path1/:'],
            [['../path2/index.html', 'another/index.html'], '#path2/:'],
            [['../index.html', 'another/index.html'], '#.:'],
            [['#hash', 'path1/index.html'], '#path1/:hash'],
            [['#hash', 'path2/index.html'], '#path2/:hash'],
            [['#hash', 'path3/index.html'], '#path3/:hash'],
        ])

        run_test('internal links with `use_directory_urls: false`', [
            # [[href, rel_url], x_href]
            [['#one', 'test.html'], '#test/:one'],
            [['#one', 'test2.html'], '#test2/:one'],
            [['test2.html#one', 'test.html'], '#test2/:one'],
            [['#one', 'path/test.html'], '#path/test/:one'],
            [['#one', 'path/sub/test.html'], '#path/sub/test/:one'],

            [['target/test.html', 'path/c.html'], '#path/target/test/:'],
            [['target/test.html#hash', 'path/c.html'], '#path/target/test/:hash'],
            [['../target/test.html', 'path/c.html'], '#target/test/:'],
            [['../target/test.html#hash', 'path/c.html'], '#target/test/:hash'],

            [['target/test.html', 'path/sub/c.html'], '#path/sub/target/test/:'],
            [['target/test.html#hash', 'path/sub/c.html'], '#path/sub/target/test/:hash'],
            [['../target/test.html', 'path/sub/c.html'], '#path/target/test/:'],
            [['../target/test.html#hash', 'path/sub/c.html'], '#path/target/test/:hash'],
            [['../../target/test.html', 'path/sub/c.html'], '#target/test/:'],
            [['../../target/test.html#hash', 'path/sub/c.html'], '#target/test/:hash'],
        ])

        run_test('what is this? will be this plugin bugs.', [
            # [[href, rel_url], x_href]
            [['../page.md/#hash', 'path/sub/'], '#path/page.md/:hash'],
        ])

        run_test('ignore cases - DO NOT CARE in this plugin.', [
            # [[href, rel_url], x_href]
            [['../', '.'], '#.:'],
            [['../', 'index.html'], '#.:'],
            [['../index.html', 'index.html'], '#.:'],
            [['../index.html#hash', 'index.html'], '#.:hash'],

            [['../../', 'path/'], '#.:'],
            [['../../', 'path/index.html'], '#.:'],
            [['../../index.html', 'path/'], '#.:'],
            [['../../index.html', 'path/index.html'], '#.:'],
            [['../../index.html#hash', 'path/index.html'], '#.:hash'],

            [['../../../', 'path/sub/'], '#.:'],
            [['../../../', 'path/sub/index.html'], '#.:'],
            [['../../../index.html', 'path/sub/'], '#.:'],
            [['../../../index.html', 'path/sub/index.html'], '#.:'],
            [['../../../index.html#hash', 'path/sub/index.html'], '#.:hash'],
            [['../../../index.html', 'path/sub.html'], '#.:'],
            [['../../../index.html', 'path/sub.html'], '#.:'],
            [['../../../index.html#hash', 'path/sub.html'], '#.:hash'],
        ])

        run_test('not internal links.', [
            # [[href, rel_url], x_href]
            [['//ex.com/test.html',            'any/index.html'],      '//ex.com/test.html'],
            [['https://ex.com/test.html',      'any/index.html'],      'https://ex.com/test.html'],
            [['https://ex.com/test.html#frag', 'any/index.html'],      'https://ex.com/test.html#frag'],
            [['mailto:ex.com/test.html',       'any/index.html'],      'mailto:ex.com/test.html'],
        ])

        run_test('path contains escape characters.', [
            # [[href, rel_url], x_href]
            [['Q&A/', '.'], '#Q%26A/:'],
            [['Progress_100%/', '.'], '#Progress_100%25/:'],
            [['Q&A/', 'any/'], '#any/Q%26A/:'],
            [['entry_ä/', 'any/'], '#any/entry_%C3%A4/:'],
            [['entry_&/', 'any/'], '#any/entry_%26/:'],
            [['../Q&A/', '.'], '#Q%26A/:'],
            [['../entry_ä/', 'any/'], '#entry_%C3%A4/:'],
            [['../entry_&/', 'any/'], '#entry_%26/:'],
            [['Q&A/', 'any/sub/'], '#any/sub/Q%26A/:'],
            [['../Q&A/', 'any/sub/'], '#any/Q%26A/:'],
            [['../Q&A/!_Answer', 'any/sub/'], '#any/Q%26A/%21_Answer:'],
            [['../sub1/Q&A/', 'any/sub/'], '#any/sub1/Q%26A/:'],
        ])
