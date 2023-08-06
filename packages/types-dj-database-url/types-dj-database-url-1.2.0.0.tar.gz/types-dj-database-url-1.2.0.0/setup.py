from setuptools import setup

name = "types-dj-database-url"
description = "Typing stubs for dj-database-url"
long_description = '''
## Typing stubs for dj-database-url

This is a PEP 561 type stub package for the `dj-database-url` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `dj-database-url`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/dj-database-url. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `92d130f6b62f6071abc267d93a22c81e091a1a18`.
'''.lstrip()

setup(name=name,
      version="1.2.0.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/dj-database-url.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['dj_database_url-stubs'],
      package_data={'dj_database_url-stubs': ['__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
