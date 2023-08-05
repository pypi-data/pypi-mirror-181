# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['testpackageforjoblibsigma']

package_data = \
{'': ['*']}

install_requires = \
['joblib>=1.2.0,<2.0.0']

entry_points = \
{'console_scripts': ['testpackageforjoblibsigma = '
                     'testpackageforjoblibsigma.cli:entry']}

setup_kwargs = {
    'name': 'testpackageforjoblibsigma',
    'version': '0.1.8',
    'description': 'test to make package and set up python environment',
    'long_description': '# Testpackage\n\n[![Apache2.0 License](https://img.shields.io/badge/License-Apatch2.0-green.svg?style=for-the-badge)](https://choosealicense.com/licenses/apache-2.0/)\n\nvscode, Github, poetryを使ったpythonの環境設定とパッケージ作成のテスト\n\n## Acknowledgements\n\n参考にしたWebページの詳細はNotionにまとめている\n\n - [Notion: Python環境設定](https://pool-laser-119.notion.site/Python-343c10792d3744c6b6c8ccf12335d5bb)\n\n## Documentation\n\nSphinxで作成したドキュメント\n\n- [Documentation](https://linktodocumentation)\n\n\n## Usage/Examples\n\n```python\nimport testpackageforjoblibsigma\n\nfunction App() {\n  return <Component />\n}\n```\n\n\n## Running Tests\n\nTo run tests, run the following command\n\n```bash\n  npm run test\n```\n\n\n## Authors\n\n- [@tk-tanab](https://github.com/tk-tanab)\n\n\n## License\n\n- [Apatch2.0](https://choosealicense.com/licenses/apache-2.0/)\n\n',
    'author': 'tk-tanab',
    'author_email': 'tk-tanab@ist.osaka-u.ac.jp',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tk-tanab/testpackage',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
