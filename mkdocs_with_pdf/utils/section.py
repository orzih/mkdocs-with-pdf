from base64 import b32encode
from uuid import uuid4


def get_section_path(section) -> str:
    if not section.is_section:
        raise "not section"

    slugs = []
    if len(section.ancestors):
        slugs = list(map(lambda sec: _section_slug(sec), section.ancestors))
        slugs.reverse()
    slugs.append(_section_slug(section))

    return '/'.join(slugs) + '/'


def _section_slug(section) -> str:
    if not section.is_section:
        raise "not section"

    slug = getattr(section, 'pdf_slug', None)
    if slug:
        return slug

    title = str(section.title).strip()
    title = title if title else str(uuid4)
    slug = b32encode(title.encode('utf-8')).rstrip(b'=').decode()
    setattr(section, 'pdf_slug', slug)

    return slug
