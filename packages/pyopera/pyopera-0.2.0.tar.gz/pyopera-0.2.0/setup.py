# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyopera', 'pyopera.opera', 'pyopera.opera.helpers']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyopera',
    'version': '0.2.0',
    'description': 'The NIH OPERA suite of models with Python specific functionality',
    'long_description': '# PyOPERA  \nThe [OPERA](https://ntp.niehs.nih.gov/whatwestudy/niceatm/comptox/ct-opera/opera.html) app was developed by the NIH to run Quantitative structure–activity/property relationship (QSAR/QSPR) models. QSAR models provide a way to predict chemical toxicology without the need of animal models (Madden et al., 2020). The NIH project spun off [a repo of OPERA models](https://github.com/kmansouri/OPERA) using MATLAB, this project uses the output of the NIH OPERA open-source project and converts it to a full Python package that is as usable as possible by Python developers.\n\n\nThis project is under active development, full documentation can be found [here](https://cabreratoxy.github.io/pyOPERA/). \n  \n# References\nMadden, J. C., Enoch, S. J., Paini, A., & Cronin, M. T. (2020). A Review of In Silico Tools as Alternatives to Animal Testing: Principles, Resources and Applications. Alternatives to Laboratory Animals, 48(4), 146–172. https://doi.org/10.1177/0261192920965977\n\n\n',
    'author': 'Manuel Cabrera',
    'author_email': 'cabrera.manuel555@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
