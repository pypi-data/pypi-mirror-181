# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mandown',
 'mandown.converter',
 'mandown.processor',
 'mandown.sources',
 'mandown.ui']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.10.0,<5.0.0',
 'feedparser>=6.0.8,<7.0.0',
 'filetype>=1.1.0,<2.0.0',
 'lxml>=4.7.1,<5.0.0',
 'natsort>=8.1.0,<9.0.0',
 'python-slugify>=6.1.2,<7.0.0',
 'requests>=2.27.0,<3.0.0',
 'typer>=0.6.0,<0.7.0']

extras_require = \
{'gui': ['PySide6>=6.4.0,<7.0.0'], 'postprocessing': ['Pillow>=9.0.1,<10.0.0']}

entry_points = \
{'console_scripts': ['mandown = mandown.cli:main',
                     'mandown-gui = mandown.ui.ui:main']}

setup_kwargs = {
    'name': 'mandown',
    'version': '1.1.1',
    'description': 'Comic/manga/webtoon downloader and converter to CBZ/EPUB/PDF',
    'long_description': '# mandown\n\n![Supported Python versions](https://img.shields.io/pypi/pyversions/mandown)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)\n[![Download from PyPI](https://img.shields.io/pypi/v/mandown)](https://pypi.org/project/mandown)\n[![Download from the AUR](https://img.shields.io/aur/version/mandown-git)](https://aur.archlinux.org/packages/mandown-git)\n[![Latest release](https://img.shields.io/github/v/release/potatoeggy/mandown?display_name=tag)](https://github.com/potatoeggy/mandown/releases/latest)\n[![License](https://img.shields.io/github/license/potatoeggy/mandown)](/LICENSE)\n\nComic downloader and converter to CBZ, EPUB, and/or PDF as a Python library and command line application.\n\n## Supported sites\n\nTo request a new site, please file a [new issue](https://github.com/potatoeggy/mandown/issues/new).\n\n- https://mangasee123.com\n- https://manganato.com\n- https://webtoons.com\n- https://mangadex.org\n- https://mangakakalot.com\n- https://readcomiconline.li\n\n## Installation\n\nInstall the package from PyPI:\n\n```\npip3 install mandown\n```\n\nInstall the optional large dependencies for some features of Mandown:\n```\n# image processing\npip3 install Pillow\n\n# graphical interface (GUI)\npip3 install PySide6\n```\n\nArch Linux users may also install the package from the [AUR](https://aur.archlinux.org/packages/mandown-git.git):\n\n```\ngit clone https://aur.archlinux.org/mandown-git.git\nmakepkg -si\n```\n\nOr, to build from source:\n\nMandown depends on [poetry](https://github.com/python-poetry/poetry) for building.\n\n```\ngit clone https://github.com/potatoeggy/mandown.git\npoetry install\npoetry build\npip3 install dist/mandown*.whl\n```\n\n## Usage\n\n```\nmandown get <URL>\n```\n\nTo convert the download contents to CBZ/EPUB, append the `--convert` option. To apply image processing to the downloaded images, append the `--process` option.\n\n```\nmandown get <URL> --convert epub --process rotate_double_pages\n```\n\nTo download only a certain range of chapters, append the `--start` and/or `--end` options.\n\n> **Note:** `--start` and `--end` are *inclusive*, i.e., using `--start 2 --end 3` will download chapters 2 and 3.\n\nTo convert an existing folder without downloading anything (like a stripped-down version of https://github.com/ciromattia/kcc), use the `convert` command.\n\n```\nmandown convert <FORMAT> <PATH_TO_FOLDER>\n```\n\nTo process an existing folder without downloading anything, use the `process` command.\n\n```\nmandown process <PROCESS_OPERATIONS> <PATH_TO_FOLDER>\n```\n\nWhere `PROCESS_OPERATIONS` is an option found from running `mandown process --help`.\n\nRun `mandown --help` for more info.\n\n## Library usage\n\nTo just download the images:\n```python\nimport mandown\n\nmandown.download("https://comic-site.com/the-best-comic")\n```\n\nTo download and convert to EPUB:\n```python\nimport mandown\n\ncomic = mandown.query("https://comic-site.com/the-best-comic")\nmandown.download(comic)\nmandown.convert(comic, comic.metadata.title, "epub")\n```\n\nMore advanced stuff:\n\n```python\nimport mandown\n\n# load a previously downloaded comic...\ncomic = mandown.load("path/to/comic/folder")\nprint(comic.metadata, comic.chapters)\n\n# ...OR fetch a comic from a source by URL\ncomic = mandown.query(url_to_comic)\nprint(comic.metadata, comic.chapters)\n\n# download the first 10 chapters of comic to ./comic using 4 threads\nmandown.download(comic, "./comic/", threads=4, end=10)\n\n# apply image post-processing to comic images in ./comic\nmandown.process("./comic/", options=["rotate_double_pages", "trim_borders"])\n\n# convert comic located in ./comic to epub, storing it in ./epubs\nmandown.convert(comic, "./comic/", "epub", "./epubs")\n```\n',
    'author': 'Daniel Chen',
    'author_email': 'danielchen04@hotmail.ca',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/potatoeggy/mandown',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
