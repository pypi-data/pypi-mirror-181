# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gaitmap_datasets',
 'gaitmap_datasets.egait_parameter_validation_2013',
 'gaitmap_datasets.egait_segmentation_validation_2014',
 'gaitmap_datasets.sensor_position_comparison_2019',
 'gaitmap_datasets.stair_ambulation_healthy_2021',
 'gaitmap_datasets.stair_ambulation_healthy_2021.scripts',
 'gaitmap_datasets.utils']

package_data = \
{'': ['*']}

install_requires = \
['c3d>=0.5.1,<0.6.0',
 'imucal>=2.3.0',
 'joblib>=1.2.0',
 'nilspodlib>=3.6.0',
 'pandas>=1.4.2',
 'scipy>=1.8.1',
 'tpcp>=0.11']

setup_kwargs = {
    'name': 'gaitmap-datasets',
    'version': '0.5.0',
    'description': 'Helper to access to open-source gait datasets used by MaD-Lab',
    'long_description': '[![PyPI](https://img.shields.io/pypi/v/gaitmap-datasets)](https://pypi.org/project/gaitmap-datasets/)\n[![Documentation status](https://img.shields.io/badge/docs-online-green)](https://mad-lab-fau.github.io/gaitmap-datasets)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/gaitmap-datasets)\n\n# gaitmap-datasets\n\nHelper to access to open-source gait datasets compatible with the MaD-Lab gaitanalysis library gaitmap.\n\nThe aim of this package is to ensure that all datasets can be loaded in a similar fashion and all data (and annotations)\nare in the same format (i.e. the same sensor orientations, units, etc.).\nThis should allow to easily run the same algorithm across multiple datasets.\n\n> :warning: While this makes it easier to work with the datasets, the coordinate system and other data information\n> provided with the dataset might not match the format you get when using this library!\n\n\nAll datasets APIs are built using the \n[`tpcp.Dataset`](https://tpcp.readthedocs.io/en/latest/modules/generated/dataset/tpcp.Dataset.html#tpcp.Dataset)\ninterface.\nFor available datasets see the table below.\n\n## Usage\n\nInstall the package from Pip\n\n```\npip install gaitmap-datasets\n```\n\nThen download/obtain the dataset that you are planning to use (see below).\nThe best way to get started is to then check the example for the respective dataset on the \n[documentation page](https://mad-lab-fau.github.io/gaitmap-datasets/auto_examples/index.html).\n\n## Datasets\n\n| Dataset                         | Info Link                                                       | Download                            |\n|---------------------------------|-----------------------------------------------------------------|-------------------------------------|\n| EgaitSegmentationValidation2014 | https://www.mad.tf.fau.de/research/activitynet/digital-biobank/ | Email to data owner (see info link) |\n| EgaitParameterValidation2013    | https://www.mad.tf.fau.de/research/activitynet/digital-biobank/ | Email to data owner (see info link) |\n| StairAmbulationHealthy2021      | https://osf.io/sgbw7/                                           | https://osf.io/download/5ueq6/      |\n| SensorPositionDataset2019       | https://zenodo.org/record/5747173                               | https://zenodo.org/record/5747173   |\n\n## Testing\n\nThe `/tests` directory contains a set of tests to check the functionality of the library.\nHowever, most tests rely on the existence of the respective datasets in certain folders outside the library.\nTherefore, the tests can only be run locally and not on the CI server.\n\nTo run them locally, make sure datasets are downloaded into the correct folders and then run `poe test`.\n\n## Documentation (build instructions)\n\nLike the tests, the documentation requires the datasets to be downloaded into the correct folders to execute the \nexamples.\nTherefore, we can not build the docs automatically on RTD.\nInstead we host the docs via github pages.\nThe HTML source can be found in the `gh-pages` branch of this repo.\n\nTo make the deplowment as easy as possible, we "mounted" the `gh-pages` branch as a submodule in the `docs/_build/html`\nfolder.\nHence, before you attempt to build the docs, you need to initialize the submodule.\n\n```\ngit submodule update --init --recursive\n```\n\nAfter that you can run `poe docs` to build the docs and then `poe upload_docs` to push the changes to the gh-pages\nbranch.\nWe will always just update a single commit on the gh-pages branch to keep the effective file size small.\n\n**WARNING: ** Don\'t delete the `docs/_build` folder manually or by running the sphinx make file!\nThis will delete the submodule and might cause issues.\nThe `poe` task is configured to clean all relevant files in the `docs/_build` folder before each run.\n\nAfter an update of the documentation, you will see that you also need to make a commit in the main repo, as the commit \nhash of the docs submodule has changed.\n\nTo make sure you don\'t forget to update the docs, the `poe prepare_release` task will also build and upload the docs \nautomatically.',
    'author': 'Arne Küderle',
    'author_email': 'arne.kuederle@fau.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mad-lab-fau/gaitmap-datasets',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
