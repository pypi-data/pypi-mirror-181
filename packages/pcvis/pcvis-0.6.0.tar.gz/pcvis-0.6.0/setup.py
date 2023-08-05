# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pcvis']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['pcvis = pcvis.pcvis:cli']}

setup_kwargs = {
    'name': 'pcvis',
    'version': '0.6.0',
    'description': '2022-12-12',
    'long_description': '# pcvis\nA command line tool for visualizing page cache status of given files\n\n# prerequisites\n* install `pcstat` (Page Cache stat: get page cache stats for files, https://github.com/tobert/pcstat)\n  * it has both Linux and macOS binaries since v0.0.1\n  * if you are using Linux/macOS, you can skip this step and use `pcvis --install-pcstat` to install it automatically\n\n# installation\n## via `pip`\n```\npip install pcvis\n```\nAfter installation, there will be a command called `pcvis` you can use\n## manual\n1. Download this repo, copy the `pcvis/pcvis.py` from this repo\n2. Move `pcvis.py` into your `$PATH` (e.g. `/usr/local/bin`)\n```\nmv pcvis.py /usr/local/bin/pcvis\nchmod +x /usr/local/bin/pcvis\n```\n\n# usage\nVisualize a given file\'s page cache status like below:\n\n```\n# pcstat still needs to be installed, and it will be automatically launched by pcvis\npcvis -f /path/to/my_file\n```\n\n\n## sample outputs\n█░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░░░░░░░░░░░░░░░░░░░█░░░░░░░░░█░░░░█░█░██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█\n\nVia this visualization, you can easily spot that:\n1. the black blocks indicate the part of the file that is in the page cache\n2. this file\'s header and footer are accessed and loaded in page cache\n3. this file is accessed in a random access manner, and you may even vaguely check if the random access is a binary search, etc\n\n## arguments\n* `-f` or `--file`: the path to the file(s) you want to visualize its page cache status, e.g. `pcvis -f /path/to/foo_file /path/to/bar_file`. If you specify this argument, `pcvis` will launch `pcstat` automatically and visualize the result. If this argument is not specified, `pcvis` will read the output of `pcstat` from `stdin`, e.g. `pcstat -json -pps /path/to/my_file | pcvis`\n* `-s` or `--style`: there are over 20 different rendering styles to choose from, you can specify a custom style by passing an integer to this argument. The default style is `0`. Some sample styles are shown below:\n\n  * e.g. `pcvis -s 3`\n🌕🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌕🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌕🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌕🌑🌑🌑🌑🌑🌑🌑🌑🌑🌕🌑🌑🌑🌑🌕🌑🌕🌑🌕🌕🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌑🌕\n  * e.g. `pcvis -s 4`\n💚🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍💚🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍💚🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍💚🤍🤍🤍🤍🤍🤍🤍🤍🤍💚🤍🤍🤍🤍💚🤍💚🤍💚💚🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍💚\n* `-i` or `--install-pcstat`: install pcstat to your system. By default, pcstat is installed into /usr/local/bin. You can specify `PCVIS_PCSTAT_PATH` env var to alter the default install dir. e.g. `PCVIS_PCSTAT_PATH=/usr/bin pcvis -i`\n* `-l` or `--list`: list all styles available\n* `-v` or `--version`: show version (only available if you install via `pip`)\n* `-h` or `--help`: show help message\n\n# examples\n1. Visualize all csv files\' page cache\n```shell\nfind . -iname "*.csv" | xargs pcvis -f\n```\n\n2. Install `pcstat` automatically into `/usr/local/bin`\n```shell\npcvis --install-pcstat\n```\n\n3. List all available styles\n```shell\npcvis --list\n```\n\n# notes\n1. If you are doing database kernel development and would like to verify IO access pattern for your files, before running the above command for visualization, you may need to clean page cache up front so that such result clearly show the IO access pattern each time\n\n```\n# for linux\nsync; echo 1 > /proc/sys/vm/drop_caches \n\n# for macOS\nsudo purge\n```\n\n2. Some of the icons in the visualization requires UTF8 to render, so you may need to set locale to UTF8 under some systems\n```\nexport LC_ALL="en_US.utf8"\n```\nOtherwise, errors like `\'ascii\' codec can\'t encode character u\'\\xa0\' in position 20: ordinal not in range(128)` may be reported.\n\nAlternatively, you may try using some ASCII only style like `pcvis -s 1 -f /path/to/file` to avoid such issue.\n\n# development\n## run tests\n```\npoetry run pytest\n```\n\n## install dev revision locally\n```\nmake setup\n```\n\n\n',
    'author': 'Yue Ni',
    'author_email': 'niyue.com@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
