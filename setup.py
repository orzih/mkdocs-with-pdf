import io

from setuptools import find_packages, setup

setup(
    name='mkdocs-with-pdf',
    version='0.8.0',
    description='Generate a single PDF file from MkDocs repository',  # noqa E501
    long_description=io.open('README.md', encoding='utf8').read(),
    long_description_content_type='text/markdown',
    keywords='mkdocs pdf weasyprint',
    url='https://github.com/orzih/mkdocs-with-pdf',
    author='orzih',
    author_email='orzih@mail.com',
    license='MIT',
    python_requires='>=3.5',
    install_requires=[
        'mkdocs>=1.1',
        'weasyprint>=0.44',
        'beautifulsoup4>=4.6.3',
        'libsass>=0.15'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'mkdocs.plugins': [
            'with-pdf = mkdocs_with_pdf.plugin:WithPdfPlugin'
        ]
    }
)
