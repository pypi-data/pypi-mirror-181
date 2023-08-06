from setuptools import setup

name = "types-dockerfile-parse"
description = "Typing stubs for dockerfile-parse"
long_description = '''
## Typing stubs for dockerfile-parse

This is a PEP 561 type stub package for the `dockerfile-parse` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `dockerfile-parse`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/dockerfile-parse. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `92d130f6b62f6071abc267d93a22c81e091a1a18`.
'''.lstrip()

setup(name=name,
      version="2.0.0.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/dockerfile-parse.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['dockerfile_parse-stubs'],
      package_data={'dockerfile_parse-stubs': ['__init__.pyi', 'constants.pyi', 'parser.pyi', 'util.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
