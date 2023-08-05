# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mdctn', 'mdctn.core']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.23.5,<2.0.0', 'scipy>=1.9.3,<2.0.0']

setup_kwargs = {
    'name': 'mdctn',
    'version': '0.3.0',
    'description': 'Multidimensional Modified Discrete Cosine Transforms',
    'long_description': '# MDCTN :yarn:\n\nMultidimensional [Modified Discrete Cosine Transforms](https://en.wikipedia.org/wiki/Modified_discrete_cosine_transform)\n\n```bash\npip install mdctn\n```\n\n- [x] 1-D MDCT & IMDCT\n- [ ] n-D MDCT & IMDCT\n- [ ] Windowing support\n- [x] Helper functions for signals\n\n\n\n### 1-D MDCT on signals\n\nSignals are [wrapped around](https://github.com/zeroby0/mdctn/discussions/1)\nso all the data is stored in the same number of bits.\n\n``` python\nimport numpy as np\nfrom mdctn import mdct, imdct\n\nx = np.arange(24)\n\ny =  mdct(x, N=16)\nz = imdct(y, N=16)\n\nnp.allclose(x, z) # True\n```\n\n### 1-D Pure MDCT\n\nThe core MDCT function\n\n``` python\nimport numpy as np\nfrom mdctn import core\n\nx = np.arange(6) # [0, 1, 2, 3, 4, 5]\n\ny_1 = core.mdct(x[0:4]) # [-2.50104055, -0.49476881]\ny_2 = core.mdct(x[2:6]) # [-4.34879961, -1.26013568]\n\nz_1 = core.imdct(y_1) # [-0.5,  0.5,  2.5,  2.5]\nz_2 = core.imdct(y_2) #             [-0.5,  0.5,  4.5,  4.5]\n\nz = (z_1[2:4] + z_2[0:2]) # [2.0, 3.0]\n```\n\n### Benchmarks\n\nSee [benchmarks.ipynb](./benchmarks.ipynb)\n\n\n\n\n',
    'author': 'Aravind Reddy Voggu',
    'author_email': 'aravind.reddy@iiitb.org',
    'maintainer': 'Aravind Reddy Voggu',
    'maintainer_email': 'aravind.reddy@iiitb.org',
    'url': 'https://github.com/zeroby0/mdctn.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
