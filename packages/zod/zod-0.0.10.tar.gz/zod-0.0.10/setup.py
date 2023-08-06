# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zod',
 'zod.frames',
 'zod.frames.evaluation.object_detection',
 'zod.frames.evaluation.object_detection.nuscenes_eval.common',
 'zod.frames.evaluation.object_detection.nuscenes_eval.detection',
 'zod.frames.polygon_annotations',
 'zod.frames.traffic_sign_classification',
 'zod.sequences.dds_parsers',
 'zod.utils',
 'zod.visualization']

package_data = \
{'': ['*'], 'zod.frames.evaluation.object_detection': ['nuscenes_eval/*']}

install_requires = \
['dataclass-wizard>=0.22.2,<0.23.0',
 'h5py>=3.1,<4.0',
 'pyquaternion>=0.9.5,<0.10.0',
 'scipy>=1.5,<2.0',
 'tqdm>=4.60,<5.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0'],
 ':python_version >= "3.8" and python_version < "4.0" and sys_platform == "darwin"': ['numpy>=1.21,<2.0',
                                                                                      'scipy>=1.9,<2.0',
                                                                                      'h5py>=3.3,<4.0'],
 'cli': ['typer[all]>=0.7.0,<0.8.0', 'dropbox>=11.36.0,<12.0.0']}

entry_points = \
{'console_scripts': ['zod = zod.main:app']}

setup_kwargs = {
    'name': 'zod',
    'version': '0.0.10',
    'description': 'Zenseact Open Dataset',
    'long_description': "# Zenseact Open Dataset\n\nTODO:  Move over stuff from the old README\n\n## Installation\n\nTo install the full devkit, including the CLI, run:\n```bash\npip install zod[cli]\n```\n\nElse, to install the library only, run:\n```bash\npip install zod\n```\n\n## Download\n\nnice little trick to download only mini version from cluster\n\n```bash\nrsync -ar --info=progress2 hal:/staging/dataset_donation/round_2/mini_train_val_single_frames.json ~/data/zod\n\ncat ~/data/zod/mini_train_val_single_frames.json | jq -r '.[] | .[] | .frame_id' | xargs -I{} rsync -ar --info=progress2 hal:/staging/dataset_donation/round_2/single_frames/{} ~/data/zod/single_frames\n```\n",
    'author': 'Zenseact',
    'author_email': 'opendataset@zenseact.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://zod.zenseact.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
