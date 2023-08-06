# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyfeyn2',
 'pyfeyn2.auto',
 'pyfeyn2.interface',
 'pyfeyn2.render',
 'pyfeyn2.render.latex',
 'pyfeyn2.render.mpl',
 'pyfeyn2.render.pyx',
 'pyfeyn2.render.text']

package_data = \
{'': ['*']}

install_requires = \
['Wand',
 'cssutils',
 'dot2tex',
 'feynman>=2.0.0',
 'graphviz',
 'ipyparallel',
 'matplotlib>=1.4.0',
 'numpy>=1.6',
 'particle',
 'pydot',
 'pygments',
 'pyhepmc',
 'pylatex',
 'pylatexenc',
 'pyx>=0.12',
 'xsdata[cli,lxml,soap]']

entry_points = \
{'console_scripts': ['mkfeyndiag = pyfeyn2.mkfeyndiag:main']}

setup_kwargs = {
    'name': 'pyfeyn2',
    'version': '2.0.7',
    'description': 'PyFeyn is a package which makes drawing Feynman diagrams simple and programmatic.  Feynman diagrams are important constructs in perturbative field theory, so being able to draw them in a programmatic fashion is important if attempting to enumerate a large number of diagram configurations is important. The output quality of PyFeyn diagrams (into PDF or EPS formats) is very high, and special effects can be obtained by using constructs from PyX, which PyFeyn is based around',
    'long_description': "# PyFeyn2\n\nForked from <https://pyfeyn.hepforge.org/> \nFeynML from <https://feynml.hepforge.org/>\n\nPyFeyn is a Python-language based system for drawing Feynman diagrams. It was inspired by the C++ FeynDiagram system, and aims to provide the same functionality and quality of output as that, with the added benefits of a modern interpreted language, an improved interface and output direct to both EPS and PDF. Behind the scenes, PyFeyn uses the excellent PyX system - you can use PyX constructs in PyFeyn diagrams if you want, too.\n\n[![PyPI version][pypi image]][pypi link] [![PyPI version][pypi versions]][pypi link]  ![downloads](https://img.shields.io/pypi/dm/smpl.svg)\n\n| [Stable][doc stable]        | [Test][doc test]           |\n| ------------- |:-------------:|\n| [![workflow][a s image]][a s link]   | [![test][a t image]][a t link]     |\n| [![Coverage Status][c s i]][c s l]   | [![Coverage Status][c t i]][c t l] |\n| [![Codacy Badge][cc s c i]][cc s c l] | [![Codacy Badge][cc c i]][cc c l]  |\n| [![Codacy Badge][cc s q i]][cc s q l] | [![Codacy Badge][cc q i]][cc q l]  |\n| [![Documentation][rtd s i]][rtd s l] | [![Documentation][rtd t i]][rtd t l]|\n\n## Dependencies\n\n*   libmagickwand-dev (to display pdfs in a jupyter-notebook, might require a policy change of the imagemagick config for PDFs, see Troubleshooting)\n*   ghostscript\n*   latexmk\n*   (feynmp-auto/feynmf)\n\n## Installation\n\n```sh\npoerty install --with docs --with dev\npoetry shell\n```\n\n## Documentation\n\n*   <https://pyfeyn2.readthedocs.io/en/stable/>\n*   <https://apn-pucky.github.io/pyfeyn2/index.html>\n\n## Similar Feynman diagram rendering project:\n\n*  <https://github.com/ndeutschmann/qgraf-xml-drawer>\n*  <https://github.com/GkAntonius/feynman>\n*  <https://github.com/JP-Ellis/tikz-feynman>\n*  <https://pyfeyn.hepforge.org/> \n*  <https://feynml.hepforge.org/>\n\nSeveral of these are integrated into pyfeyn2.\n\n## Troubleshooting\n\n*   [ImageMagick security policy 'PDF' blocking conversion]( https://stackoverflow.com/questions/52998331/imagemagick-security-policy-pdf-blocking-conversion )\n\n## Development\n\n\n### package/python structure:\n\n*   <https://mathspp.com/blog/how-to-create-a-python-package-in-2022>\n*   <https://www.brainsorting.com/posts/publish-a-package-on-pypi-using-poetry/>\n\n[doc stable]: https://apn-pucky.github.io/pyfeyn2/index.html\n[doc test]: https://apn-pucky.github.io/pyfeyn2/test/index.html\n\n[pypi image]: https://badge.fury.io/py/pyfeyn2.svg\n[pypi link]: https://pypi.org/project/pyfeyn2/\n[pypi versions]: https://img.shields.io/pypi/pyversions/pyfeyn2.svg\n\n[a s image]: https://github.com/APN-Pucky/pyfeyn2/actions/workflows/stable.yml/badge.svg\n[a s link]: https://github.com/APN-Pucky/pyfeyn2/actions/workflows/stable.yml\n[a t link]: https://github.com/APN-Pucky/pyfeyn2/actions/workflows/test.yml\n[a t image]: https://github.com/APN-Pucky/pyfeyn2/actions/workflows/test.yml/badge.svg\n\n[cc s q i]: https://app.codacy.com/project/badge/Grade/135bae47c6344ab0bfb180135ea1db44?branch=stable\n[cc s q l]: https://www.codacy.com/gh/APN-Pucky/pyfeyn2/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=APN-Pucky/pyfeyn2&amp;utm_campaign=Badge_Grade?branch=stable\n[cc s c i]: https://app.codacy.com/project/badge/Coverage/135bae47c6344ab0bfb180135ea1db44?branch=stable\n[cc s c l]: https://www.codacy.com/gh/APN-Pucky/smpl/dashboard?utm_source=github.com&utm_medium=referral&utm_content=APN-Pucky/pyfeyn2&utm_campaign=Badge_Coverage?branch=stable\n\n[cc q i]: https://app.codacy.com/project/badge/Grade/135bae47c6344ab0bfb180135ea1db44\n[cc q l]: https://www.codacy.com/gh/APN-Pucky/pyfeyn2/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=APN-Pucky/pyfeyn2&amp;utm_campaign=Badge_Grade\n[cc c i]: https://app.codacy.com/project/badge/Coverage/135bae47c6344ab0bfb180135ea1db44\n[cc c l]: https://www.codacy.com/gh/APN-Pucky/pyfeyn2/dashboard?utm_source=github.com&utm_medium=referral&utm_content=APN-Pucky/pyfeyn2&utm_campaign=Badge_Coverage\n\n[c s i]: https://coveralls.io/repos/github/APN-Pucky/pyfeyn2/badge.svg?branch=stable\n[c s l]: https://coveralls.io/github/APN-Pucky/pyfeyn2?branch=stable\n[c t l]: https://coveralls.io/github/APN-Pucky/pyfeyn2?branch=master\n[c t i]: https://coveralls.io/repos/github/APN-Pucky/pyfeyn2/badge.svg?branch=master\n\n[rtd s i]: https://readthedocs.org/projects/pyfeyn2/badge/?version=stable\n[rtd s l]: https://pyfeyn2.readthedocs.io/en/stable/?badge=stable\n[rtd t i]: https://readthedocs.org/projects/pyfeyn2/badge/?version=latest\n[rtd t l]: https://pyfeyn2.readthedocs.io/en/latest/?badge=latest\n",
    'author': 'Alexander Puck Neuwirth',
    'author_email': 'alexander@neuwirth-informatik.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/APN-Pucky/pyfeyn2',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
