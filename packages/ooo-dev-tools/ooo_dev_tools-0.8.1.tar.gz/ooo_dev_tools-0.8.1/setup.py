# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ooodev',
 'ooodev.adapter',
 'ooodev.adapter.awt',
 'ooodev.adapter.frame',
 'ooodev.adapter.lang',
 'ooodev.adapter.util',
 'ooodev.adapter.view',
 'ooodev.cfg',
 'ooodev.conn',
 'ooodev.dialog',
 'ooodev.events',
 'ooodev.events.args',
 'ooodev.events.args.calc',
 'ooodev.exceptions',
 'ooodev.formatters',
 'ooodev.lazy',
 'ooodev.listeners',
 'ooodev.meta',
 'ooodev.mock',
 'ooodev.office',
 'ooodev.proto',
 'ooodev.utils',
 'ooodev.utils.data_type',
 'ooodev.utils.decorator',
 'ooodev.utils.dispatch',
 'ooodev.utils.kind',
 'ooodev.wrapper']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.2.0,<10.0.0', 'lxml>=4.9.1,<5.0.0', 'ooouno>=0.2.4,<0.3.0']

extras_require = \
{':python_version < "3.8"': ['typing-extensions>=4.4.0,<5.0.0']}

setup_kwargs = {
    'name': 'ooo-dev-tools',
    'version': '0.8.1',
    'description': 'LibreOffice Developer Tools',
    'long_description': "OOO Development Tools\n=====================\n\n|lic| |pver| |pwheel| |github|\n\nOOO Development Tools (ODEV) is intended for programmers who want to learn and use the\nPython version of the `LibreOffice`_ API.\n\nThis allows Python to control and manipulate LibreOffice's text, drawing, presentation, spreadsheet, and database applications,\nand a lot more (e.g. its spell checker, forms designer, and charting tools).\n\nOne of the aims is to develop utility code to help flatten the steep learning curve for the API.\nFor example, The Lo class simplifies the steps needed to initialize the API\n(by creating a connection to a LibreOffice process), to open/create a document, save it,\nand close down LibreOffice.\n\nCurrently this project has been tested on LibreOffice in Windows and Linux (Ubuntu).\n\nAdvantages of Python\n--------------------\n\nMacros are pieces of programming code that runs in office suites and helps automate routine tasks.\nSpecifically, in LibreOffice API these codes can be written with so many programming languages thanks\nto the Universal Network Objects (UNO).\n\nSince LibreOffice is multi-platform we can use our documents at different\nplatforms like Mac, Windows, and Linux. So we need a cross-platform language to run our macros at different\nplatforms.\n\nPython has the advantage that it is cross-platform and can run inside the office environment as macros and outside\noffice environment on the command line.\n\nPython has a vast set `libraries <https://pypi.org/>`_ that can be used in a project, including `Numpy <https://numpy.org/>`_ and\n`Numexpr <https://github.com/pydata/numexpr>`_ which are excellent and powerful at numeric computation.\n\nThis makes Python and excellent choice with maximum flexibility.\n\n\nDocumentation\n-------------\n\nRead `documentation <https://python-ooo-dev-tools.readthedocs.io/en/latest/>`_\n\n\nInstallation\n------------\n\nPIP\n^^^\n\n**ooo-dev-tools** `PyPI <https://pypi.org/project/ooo-dev-tools/>`_\n\n.. code-block:: bash\n\n    $ pip install ooo-dev-tools\n\n\nModules\n-------\n\nInclude modules:\n    - Calc (Calc)\n    - Write (Write)\n    - Draw (LibreOffice Draw/Impress)\n    - Forms (Support for building forms)\n    - Dialogs (Build dialog forms)\n    - GUI (Various GUI methods for manipulating LO Windows)\n    - Lo (Various methods common to LO applications)\n    - FileIO (File Input and Output for working with LO)\n    - Props (Various methods setting and getting the many properties of Office objects)\n    - Info (Various method for getting information about LO applications)\n    - Color (Various color utils)\n    - DateUtil (Date Time utilities)\n    - ImagesLo (Various methods for working with Images)\n    - Props (Various methods for working with the many API properties)\n    - Chart2 (charting)\n    - Chart (charting)\n    - And more ...\n\nFuture releases will add:\n    - Base (LibreOffice Base)\n    - Clip (clipboard support)\n    - Gallery (Methods for accessing and reporting on the Gallery)\n    - Mail (Mail service provider)\n    - Print (Print service provider)\n    - And more ...\n\nInspiration\n-----------\n\nMuch of this project is inspired by the work of Dr. Andrew Davison\nand the work on `Java LibreOffice Programming <http://fivedots.coe.psu.ac.th/~ad/jlop>`_\n\nSee `LibreOffice Programming <https://flywire.github.io/lo-p/>`_ that aims to gradually explain this content in a python context.\n\n\nOther\n-----\n\n**Figure 1:** Calc Find and Replace Automation Example\n\n.. figure:: https://user-images.githubusercontent.com/4193389/172609472-536a94de-9bf6-4668-ac9f-a55f12dfc817.gif\n    :alt: Calc Find and Replace Automation\n\n\nRelated projects\n----------------\n\nLibreOffice API Typing's\n\n * `LibreOffice API Typings <https://github.com/Amourspirit/python-types-unopy>`_\n * `ScriptForge Typings <https://github.com/Amourspirit/python-types-scriptforge>`_\n * `Access2base Typings <https://github.com/Amourspirit/python-types-access2base>`_\n * `LibreOffice UNO Typings <https://github.com/Amourspirit/python-types-uno-script>`_\n * `LibreOffice Developer Search <https://github.com/Amourspirit/python_lo_dev_search>`_\n * `LibreOffice Python UNO Examples <https://github.com/Amourspirit/python-ooouno-ex>`_\n * `OOOUNO Project <https://github.com/Amourspirit/python-ooouno>`_\n * `OOO UNO TEMPLATE <https://github.com/Amourspirit/ooo_uno_tmpl>`_\n\n.. _LibreOffice: http://www.libreoffice.org/\n\n.. |lic| image:: https://img.shields.io/github/license/Amourspirit/python_ooo_dev_tools\n    :alt: License Apache\n\n.. |pver| image:: https://img.shields.io/pypi/pyversions/ooo-dev-tools\n    :alt: PyPI - Python Version\n\n.. |pwheel| image:: https://img.shields.io/pypi/wheel/ooo-dev-tools\n    :alt: PyPI - Wheel\n\n.. |github| image:: https://img.shields.io/badge/GitHub-100000?style=plastic&logo=github&logoColor=white\n    :target: https://github.com/Amourspirit/python_ooo_dev_tools\n    :alt: Github",
    'author': ':Barry-Thomas-Paul: Moss',
    'author_email': 'bigbytetech@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Amourspirit/python_ooo_dev_tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
