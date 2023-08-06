# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sparrow',
 'sparrow.algorithm',
 'sparrow.ann',
 'sparrow.api',
 'sparrow.cli',
 'sparrow.color',
 'sparrow.cv',
 'sparrow.datasets',
 'sparrow.debug',
 'sparrow.decorators',
 'sparrow.distance',
 'sparrow.doc',
 'sparrow.docker',
 'sparrow.functions',
 'sparrow.inspect',
 'sparrow.io',
 'sparrow.jupyter',
 'sparrow.jupyter.utils',
 'sparrow.log',
 'sparrow.math',
 'sparrow.math.sampling',
 'sparrow.multiprocess',
 'sparrow.multiprocess.mq',
 'sparrow.ner',
 'sparrow.net',
 'sparrow.nn',
 'sparrow.path',
 'sparrow.performance',
 'sparrow.progress_bar',
 'sparrow.proto',
 'sparrow.proto.python',
 'sparrow.proxy',
 'sparrow.string',
 'sparrow.table_ops',
 'sparrow.template',
 'sparrow.template.scaffold',
 'sparrow.template.scaffold.src',
 'sparrow.template.scaffold.src.project_name',
 'sparrow.template.scaffold.src.project_name.api',
 'sparrow.template.scaffold.src.project_name.api.routes',
 'sparrow.template.scaffold.src.tests',
 'sparrow.transform',
 'sparrow.trie',
 'sparrow.utils',
 'sparrow.web',
 'sparrow.widgets']

package_data = \
{'': ['*'],
 'sparrow.ann': ['milvus_db/*'],
 'sparrow.api': ['static/*'],
 'sparrow.log': ['conf/*'],
 'sparrow.proto': ['js/*'],
 'sparrow.template.scaffold.src': ['Examples/*', 'conf/*', 'docker/*'],
 'sparrow.web': ['.streamlit/*']}

install_requires = \
['Deprecated',
 'GitPython',
 'attrs>=22.1.0,<23.0.0',
 'chevron',
 'colour',
 'concurrent-log-handler',
 'fire',
 'gpustat>=1.0.0,<2.0.0',
 'numpy',
 'pandas>=1.5.0,<2.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'pretty_errors>=1.2.25,<2.0.0',
 'psutil>=5.9.2,<6.0.0',
 'pyyaml',
 'rich']

entry_points = \
{'console_scripts': ['spr = sparrow.__main__:main']}

setup_kwargs = {
    'name': 'sparrow-tool',
    'version': '0.8.1',
    'description': '',
    'long_description': '# sparrow_tool\n[![image](https://img.shields.io/badge/Pypi-0.8.1-green.svg)](https://pypi.org/project/sparrow_tool)\n[![image](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/)\n[![image](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)\n[![image](https://img.shields.io/badge/author-kunyuan-orange.svg?style=flat-square&logo=appveyor)](https://github.com/beidongjiedeguang)\n\n\n-------------------------\n## Install\n```bash\npip install sparrow-tool\n# Or dev version\npip install sparrow-tool[dev]\n# Or\npip install -e .\n# Or\npip install -e .[dev]\n```\n\n\n## Usage\n\n### Safe logger in `multiprocessing`\n```python\nfrom sparrow.log import Logger\nimport numpy as np\nlogger = Logger(name=\'train-log\', log_dir=\'./logs\', )\nlogger.info("hello","numpy:",np.arange(10))\n\nlogger2 = Logger.get_logger(\'train-log\')\nprint(id(logger2) == id(logger))\n>>> True\n```\n\n### Multiprocessing SyncManager\n\nOpen server first:\n```bash\n$ sparrow start-server\n```\nThe defualt port `50001`.\n\n(Process1) productor:\n```python\nfrom sparrow.multiprocess.client import Client\nclient = Client(port=50001)\nclient.update_dict({\'a\': 1, \'b\': 2})\n```\n\n(Process2) consumer:\n```python\nfrom sparrow.multiprocess.client import Client\nclient = Client(port=50001)\nprint(client.get_dict_data())\n\n>>> {\'a\': 1, \'b\': 2}\n```\n\n### Common tools\n- **Kill process by port**\n    ```bash\n    $ sparrow kill {port}\n    ```\n\n- **pack & unpack**  \n    support archive format: "zip", "tar", "gztar", "bztar", or "xztar".\n    ```bash\n    sparrow pack pack_dir \n    sparrow unpack filename extract_dir\n    ```\n',
    'author': 'kunyuan',
    'author_email': 'beidongjiedeguang@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/beidongjiedeguang/sparrow',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.0,<4',
}


setup(**setup_kwargs)
