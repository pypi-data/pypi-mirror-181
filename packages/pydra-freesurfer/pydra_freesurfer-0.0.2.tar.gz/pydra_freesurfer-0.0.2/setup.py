# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydra', 'pydra.tasks.freesurfer']

package_data = \
{'': ['*']}

install_requires = \
['pydra>=0.21,<0.22']

setup_kwargs = {
    'name': 'pydra-freesurfer',
    'version': '0.0.2',
    'description': 'Pydra tasks for FreeSurfer',
    'long_description': "# pydra-freesurfer\n\nPydra tasks for FreeSurfer.\n\n[Pydra] is a dataflow engine which provides a set of lightweight abstractions\nfor DAG construction, manipulation, and distributed execution.\n\n[FreeSurfer] is a neuroimaging toolkit for processing, analyzing, and\nvisualizing human brain MR images.\n\nThis project exposes some of FreeSurfer's utilities as Pydra tasks to\nfacilitate their incorporation into more advanced processing workflows.\n\n## Available interfaces\n\n- gtmseg\n- mri_convert\n- mri_surf2surf\n- mri_vol2vol\n- mris_expand\n- mris_preproc\n- recon-all\n- tkregister2\n\n## Development\n\nThis project is managed using [Poetry].\n\nTo install, check and test the code:\n\n```console\nmake\n```\n\nTo run the test suite when hacking:\n\n```console\nmake test\n```\n\nTo format the code before review:\n\n```console\nmake format\n```\n\nTo build the project's documentation:\n\n```console\nmake docs\n```\n\n## Licensing\n\nThis project is released under the terms of the Apache License 2.0.\n\n\n[Pydra]: https://nipype.github.io/pydra\n[Freesurfer]: https://surfer.nmr.mgh.harvard.edu\n[Poetry]: https://python-poetry.org\n",
    'author': 'The Aramis Lab',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/aramis-lab/pydra-freesurfer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
