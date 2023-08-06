# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poppy',
 'poppy.pop',
 'poppy.pop.alembic',
 'poppy.pop.commands',
 'poppy.pop.json_schemas',
 'poppy.pop.models',
 'poppy.pop.models.versions',
 'poppy.pop.scripts']

package_data = \
{'': ['*']}

install_requires = \
['poppy-core>=0.10']

entry_points = \
{'console_scripts': ['pop = poppy.pop.scripts:main']}

setup_kwargs = {
    'name': 'poppy-pop',
    'version': '0.9.0',
    'description': 'POPPY Operation Plugin (POP)',
    'long_description': 'poppy.pop\n=========\n\n[![pipeline status](https://gitlab.obspm.fr/POPPY/POP/badges/develop/pipeline.svg)](https://gitlab.obspm.fr/POPPY/POP/pipelines)\n\n\nIntroduction\n------------\n\nThis directory contains the source code of the POPPY Operation Plugin (POP), the main plugin to be used with the POPPY framework.\n\nSee "POPPY User Manual" for more details.\n\nLicense\n-------\nPOPPY is under GPL license.\n\nAcknowledgement\n-----------\nPOPPY is project developed by the RPW Operations Centre (ROC) team based at LESIA (Meudon, France).\nThe ROC is funded by the Centre National d\'Etudes Spatiale (CNES) in the framework of the European Space Agency (ESA) Solar Orbiter mission.\n\nContact\n-------\nxavier.bonnin@obspm.fr (project manager)\nsonny.lion@obspm.fr (software designer)\nquynh-nhu.nguyen@obspm.fr (software developer)\n\ncontributors\n------------\nGregoire Duvauchelle (software developer)\nManual Duarte (software designer)\n',
    'author': 'Xavier Bonnin',
    'author_email': 'xavier.bonnin@obspm.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.obspm.fr/POPPy/POP',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
