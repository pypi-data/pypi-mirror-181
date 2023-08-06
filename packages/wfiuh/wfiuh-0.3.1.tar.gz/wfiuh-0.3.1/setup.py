# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wfiuh',
 'wfiuh.best_sample',
 'wfiuh.curve_fitting',
 'wfiuh.curve_fitting.models',
 'wfiuh.log',
 'wfiuh.param_distribution']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'matplotlib>=3.6.2,<4.0.0',
 'numpy>=1.23.4,<2.0.0',
 'pandas>=1.5.1,<2.0.0',
 'rich>=12.6.0,<13.0.0',
 'scikit-learn>=1.1.3,<2.0.0',
 'scipy>=1.9.3,<2.0.0',
 'seaborn>=0.12.1,<0.13.0']

setup_kwargs = {
    'name': 'wfiuh',
    'version': '0.3.1',
    'description': 'Curve fitting width function IUH (WFIUH) in Hydrology',
    'long_description': '# WFIUH\n\nCurve fitting width function IUH (WFIUH) in Hydrology\n\nResults can be found [here](https://drive.liblaf.top/share/WFIUH/results/).\n\n## CDF\n\n| Model              | Success Fits  |\n| ------------------ | ------------- |\n| Beta               | 11069 / 11069 |\n| DoublePower        | 11066 / 11069 |\n| DoubleTriangular   | 11069 / 11069 |\n| Frechet            | 11062 / 11069 |\n| Gamma              | 11062 / 11069 |\n| Hill               | 11059 / 11069 |\n| Hoerl              | 11069 / 11069 |\n| InverseGaussian    | 11066 / 11069 |\n| Kumaraswamy        | 11069 / 11069 |\n| Logistic           | 11062 / 11069 |\n| Multistage         | 11065 / 11069 |\n| NormalGaussian     | 11069 / 11069 |\n| Polynomial         | 11069 / 11069 |\n| Rational           | 11069 / 11069 |\n| ShiftedLogPearson3 | 11051 / 11069 |\n| Weibull            | 11069 / 11069 |\n\n## PDF\n\n| Model              | Success Fits  |\n| ------------------ | ------------- |\n| Beta               | 11061 / 11069 |\n| DoublePower        | 11065 / 11069 |\n| DoubleTriangular   | 11063 / 11069 |\n| Frechet            | 11039 / 11069 |\n| Gamma              | 11065 / 11069 |\n| Hill               | 11068 / 11069 |\n| Hoerl              | 11059 / 11069 |\n| InverseGaussian    | 11064 / 11069 |\n| Kumaraswamy        | 11069 / 11069 |\n| Logistic           | 10754 / 11069 |\n| Multistage         | 11065 / 11069 |\n| NormalGaussian     | 11069 / 11069 |\n| Polynomial         | 11069 / 11069 |\n| Rational           | 11064 / 11069 |\n| ShiftedLogPearson3 | 11027 / 11069 |\n| Weibull            | 11065 / 11069 |\n',
    'author': 'Qin Li',
    'author_email': 'liblaf@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://liblaf.github.io/WFIUH/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
