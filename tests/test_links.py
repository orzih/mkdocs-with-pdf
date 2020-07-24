import unittest

from mkdocs_with_pdf.preprocessor.links.transform import transform_href


class TransformHrefTestCase(unittest.TestCase):

    def test_transform_href(self):

        patterns = [
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

            [['../page.md/#hash', 'path/sub/'], '#page/:hash'],

            [['page.html', 'index.html'], '#page.html:'],
            [['page.html#hash', 'index.html'], '#page:hash'],
            [['page.html', 'other.html'], '#page.html:'],
        ]

        for pattern in patterns:
            case, x_href = pattern
            href, rel_url = case

            r = transform_href(href, rel_url)
            self.assertEqual(r, x_href, f"rel_url='{rel_url}', href='{href}'")
