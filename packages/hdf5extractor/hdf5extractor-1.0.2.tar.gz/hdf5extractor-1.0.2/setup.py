# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['hdf5extractor']

package_data = \
{'': ['*']}

install_requires = \
['etpproto>=1.0.1,<2.0.0',
 'h5py>=3.7.0,<4.0.0',
 'lxml>=4.6.3,<5.0.0',
 'requests>=2.25.1,<3.0.0',
 'websocket-client>=1.0.0,<2.0.0']

entry_points = \
{'console_scripts': ['extracth5-etp = hdf5extractor.etp.extract_etp:main',
                     'extracth5-local = hdf5extractor.extract_local:main']}

setup_kwargs = {
    'name': 'hdf5extractor',
    'version': '1.0.2',
    'description': 'Extract datasets from a h5 file, depending on referenced dataset from a xml file.',
    'long_description': '# hdf5-extractor\n\nExtract mini hdf5 files from an epc and an H5 file. \nThe mini-h5 are created by finding Datasets referenced from the epc. Each representation will have its own mini-h5 file.\n\n# installation :\n\n## With poetry :\n\n```console\npoetry add hdf5extractor\n```\n\n## With pip :\n\n```console\npip install hdf5extractor\n```\n\n# Run :\n\nExtract a small h5 from a bigger one, to only have dataset of a specific resqml file : \n```console\nextracth5 -i myResqmlFile.xml --h5 myH5File.h5 -o outputFolder\n```\n\nExtract every h5 parts from a bigger one, to only have in each, the dataset of a specific resqml file inside an epc : \n```console\nextracth5 -i myEPCFile.epc --h5 myH5File.h5 -o outputFolder\n```',
    'author': 'Valentin Gauthier',
    'author_email': 'valentin.gauthier@geosiris.com',
    'maintainer': 'Valentin Gauthier',
    'maintainer_email': 'valentin.gauthier@geosiris.com',
    'url': 'http://www.geosiris.com',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
