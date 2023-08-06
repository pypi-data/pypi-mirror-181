from setuptools import setup

name = "types-python-dateutil"
description = "Typing stubs for python-dateutil"
long_description = '''
## Typing stubs for python-dateutil

This is a PEP 561 type stub package for the `python-dateutil` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `python-dateutil`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/python-dateutil. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `bff43b53e50adf873c20faebb125a5fe808d4ad6`.
'''.lstrip()

setup(name=name,
      version="2.8.19.5",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/python-dateutil.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['dateutil-stubs'],
      package_data={'dateutil-stubs': ['__init__.pyi', '_common.pyi', 'easter.pyi', 'parser/__init__.pyi', 'parser/isoparser.pyi', 'relativedelta.pyi', 'rrule.pyi', 'tz/__init__.pyi', 'tz/_common.pyi', 'tz/tz.pyi', 'utils.pyi', 'zoneinfo/__init__.pyi', 'zoneinfo/rebuild.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
