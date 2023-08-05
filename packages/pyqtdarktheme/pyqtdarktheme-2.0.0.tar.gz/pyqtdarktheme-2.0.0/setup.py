# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qdarktheme',
 'qdarktheme._icon',
 'qdarktheme._resources',
 'qdarktheme._template',
 'qdarktheme.qtpy',
 'qdarktheme.qtpy.QtCore',
 'qdarktheme.qtpy.QtGui',
 'qdarktheme.qtpy.QtSvg',
 'qdarktheme.qtpy.QtWidgets',
 'qdarktheme.widget_gallery',
 'qdarktheme.widget_gallery._ui']

package_data = \
{'': ['*'], 'qdarktheme.widget_gallery': ['svg/*']}

install_requires = \
['darkdetect>=0.7.1,<0.8.0']

setup_kwargs = {
    'name': 'pyqtdarktheme',
    'version': '2.0.0',
    'description': 'Flat dark theme for PySide and PyQt.',
    'long_description': '# PyQtDarkTheme\n\nPyQtDarkTheme applies a flat dark theme to QtWidgets application(PySide and PyQt). There\'s a light theme too. Color and style balanced from a dark theme for easy viewing in daylight.\n\nCheck out the [complete documentation](https://pyqtdarktheme.readthedocs.io).\n\n**Project status**\n[![PyPI Latest Release](https://img.shields.io/pypi/v/pyqtdarktheme.svg?color=orange)](https://pypi.org/project/pyqtdarktheme/)\n[![Python Versions](https://img.shields.io/pypi/pyversions/pyqtdarktheme.svg?color=blue)](https://www.python.org/downloads/)\n[![Qt Versions](https://img.shields.io/badge/Qt-5%20|%206-blue.svg?&logo=Qt&logoWidth=18&logoColor=white)](https://www.qt.io/qt-for-python)\n[![License](https://img.shields.io/github/license/5yutan5/PyQtDarkTheme.svg?color=green)](https://github.com/5yutan5/PyQtDarkTheme/blob/main/LICENSE.txt/)\n\n**Tests**\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/5yutan5/PyQtDarkTheme/main.svg)](https://results.pre-commit.ci/latest/github/5yutan5/PyQtDarkTheme/main)\n[![codecov](https://codecov.io/gh/5yutan5/PyQtDarkTheme/branch/main/graph/badge.svg?token=RTS8O0V6SF)](https://codecov.io/gh/5yutan5/PyQtDarkTheme)\n[![Total alerts](https://img.shields.io/lgtm/alerts/g/5yutan5/PyQtDarkTheme.svg?logo=lgtm&logoWidth=18&color=success)](https://lgtm.com/projects/g/5yutan5/PyQtDarkTheme/alerts/)\n[![Documentation Status](https://readthedocs.org/projects/pyqtdarktheme/badge/?version=latest)](https://pyqtdarktheme.readthedocs.io/en/latest/?badge=latest)\n\n## Features\n\n- A flat dark and light theme\n- Support PySide and PyQt\n- Support PyInstaller\n- Sync with OS\'s theme (Mac, Windows, Linux)\n- Resolve the style differences between Qt versions\n- Provide dark/light theme QPalette\n- Override Qt old standard icons\n\n## Themes\n\n### Dark Theme\n\n![widget_gallery_dark_theme](https://raw.githubusercontent.com/5yutan5/PyQtDarkTheme/main/images/widget_gallery_dark.png)\n\n### Light Theme\n\n![widget_gallery_light_them](https://raw.githubusercontent.com/5yutan5/PyQtDarkTheme/main/images/widget_gallery_light.png)\n\n## Requirements\n\n- [Python 3.7+](https://www.python.org/downloads/)\n- Qt 5.15+\n- PySide6, PyQt6, PyQt5 or PySide2\n\n## Installation Method\n\n- Last released version\n\n   ```plaintext\n   pip install pyqtdarktheme\n   ```\n\n- Latest development version\n\n   ```plaintext\n   pip install git+https://github.com/5yutan5/PyQtDarkTheme.git@main\n   ```\n\n## Usage\n\n```Python\nimport sys\n\nfrom PySide6.QtWidgets import QApplication, QMainWindow, QPushButton\n\nimport qdarktheme\n\napp = QApplication(sys.argv)\n# Apply the complete dark theme to your Qt App.\nqdarktheme.setup_theme()\n\nmain_win = QMainWindow()\npush_button = QPushButton("PyQtDarkTheme!!")\nmain_win.setCentralWidget(push_button)\n\nmain_win.show()\n\napp.exec()\n```\n\nFurther information can be found in our docs:\n\n- [Usage Guide](https://pyqtdarktheme.readthedocs.io/en/latest/how_to_use.html)\n\n### Enable HiDPI\n\n```Python\n# enable_hi_dpi() must be called before instantiation of QApplication.\nqdarktheme.enable_hi_dpi()\napp = QApplication(sys.argv)\nqdarktheme.setup_theme()\n```\n\nFor Qt6 bindings, HiDPI “just works” without using this function.\n\n### Light theme\n\n```Python\nqdarktheme.setup_theme("light")\n```\n\n### Sync with OS\'s theme\n\n```Python\nqdarktheme.setup_theme("auto")\n```\n\n![sync with os theme](https://raw.githubusercontent.com/5yutan5/PyQtDarkTheme/main/images/sync_with_os_theme.gif)\n\n### Customizing colors\n\nYou can customize theme color.\n\n```python\n# Customize accent color.\nqdarktheme.setup_theme(custom_colors={"primary": "#D0BCFF"})\n```\n\nFurther information for customizing color can be found in our theme color docs:\n\n- [Theme Color](https://pyqtdarktheme.readthedocs.io/en/latest/reference/theme_color.html)\n\n### Sharp frame\n\nYou can change the corner style.\n\n```python\n# Default is "rounded".\nstylesheet = qdarktheme.setup_theme(corner_shape="sharp")\n```\n\n### QPalette and stylesheet\n\nYou can also only load QPalette and stylesheet. `qdarktheme.setup_theme` uses following functions internally.\n\n```Python\npalette = qdarktheme.load_palette(theme="dark")\nstylesheet = qdarktheme.load_stylesheet(theme="dark")\n```\n\n## Example\n\nTo check all Qt widgets, run:\n\n```plaintext\npython -m qdarktheme.widget_gallery\n```\n\n## License\n\nThe svg files for the PyQtDarkTheme are derived [Material design icons](https://fonts.google.com/icons)(Apache License Version 2.0). Qt stylesheets are originally fork of [QDarkStyleSheet](https://github.com/ColinDuquesnoy/QDarkStyleSheet)(MIT License). Other files are covered by PyQtDarkTheme\'s MIT license.\n\n## Contributing\n\nAll contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome. You can get started by reading this:\n\n- [Contributing Guide](https://pyqtdarktheme.readthedocs.io/en/latest/contributing.html)\n\n## Change log\n\nSee [Releases](https://github.com/5yutan5/PyQtDarkTheme/releases).\n',
    'author': 'Yunosuke Ohsugi',
    'author_email': '63651161+5yutan5@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/5yutan5/PyQtDarkTheme',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.12',
}


setup(**setup_kwargs)
