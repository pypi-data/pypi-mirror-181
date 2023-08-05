# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scikeras', 'scikeras.utils']

package_data = \
{'': ['*']}

install_requires = \
['packaging>=0.21', 'scikit-learn>=1.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=3'],
 ':python_version >= "3.10" and sys_platform == "darwin"': ['grpcio<1.50.0'],
 'tensorflow': ['tensorflow>=2.11.0'],
 'tensorflow-cpu': ['tensorflow-cpu>=2.11.0']}

setup_kwargs = {
    'name': 'scikeras',
    'version': '0.10.0',
    'description': 'Scikit-Learn API wrapper for Keras.',
    'long_description': '# Scikit-Learn Wrapper for Keras\n\n[![Build Status](https://github.com/adriangb/scikeras/workflows/Tests/badge.svg)](https://github.com/adriangb/scikeras/actions?query=workflow%3ATests+branch%3Amaster)\n[![Coverage Status](https://codecov.io/gh/adriangb/scikeras/branch/master/graph/badge.svg)](https://codecov.io/gh/adriangb/scikeras)\n[![Docs](https://github.com/adriangb/scikeras/workflows/Build%20Docs/badge.svg)](https://www.adriangb.com/scikeras/)\n\nScikit-Learn compatible wrappers for Keras Models.\n\n## Why SciKeras\n\nSciKeras is derived from and API compatible with `tf.keras.wrappers.scikit_learn`. The original TensorFlow (TF) wrappers are not actively maintained,\nand [will be removed](https://github.com/tensorflow/tensorflow/pull/36137#issuecomment-726271760) in a future release.\n\nAn overview of the advantages and differences as compared to the TF wrappers can be found in our\n[migration](https://www.adriangb.com/scikeras/stable/migration.html) guide.\n\n## Installation\n\nThis package is available on PyPi:\n\n```bash\n# Normal tensorflow\npip install scikeras[tensorflow]\n\n# or tensorflow-cpu\npip install scikeras[tensorflow-cpu]\n```\n\nSciKeras packages TensorFlow as an optional dependency because there are\nseveral flavors of TensorFlow available (`tensorflow`, `tensorflow-cpu`, etc.).\nDepending on _one_ of them in particular disallows the usage of the other, which is why\nthey need to be optional.\n\n`pip install scikeras[tensorflow]` is basically equivalent to `pip install scikeras tensorflow`\nand is offered just for convenience. You can also install just SciKeras with\n`pip install scikeras`, but you will need a version of tensorflow installed at\nruntime or SciKeras will throw an error when you try to import it.\n\nThe current version of SciKeras depends on `scikit-learn>=1.0.0` and `TensorFlow>=2.7.0`.\n\n### Migrating from `tf.keras.wrappers.scikit_learn`\n\nPlease see the [migration](https://www.adriangb.com/scikeras/stable/migration.html) section of our documentation.\n\n## Documentation\n\nDocumentation is available at [https://www.adriangb.com/scikeras/](https://www.adriangb.com/scikeras/).\n\n## Contributing\n\nSee [CONTRIBUTING.md](https://github.com/adriangb/scikeras/blob/master/CONTRIBUTING.md)\n',
    'author': 'Adrian Garcia Badaracco',
    'author_email': '1755071+adriangb@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/adriangb/scikeras',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.0,<3.11.0',
}


setup(**setup_kwargs)
