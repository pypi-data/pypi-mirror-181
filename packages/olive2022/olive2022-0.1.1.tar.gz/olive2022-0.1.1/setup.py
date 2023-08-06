# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['olive2022']
install_requires = \
['sinfonia-tier3>=0.6.0,<0.7.0', 'tqdm>=4.64.1,<5.0.0', 'xdg>=5.1.1,<6.0.0']

entry_points = \
{'console_scripts': ['olive2022 = olive2022:main']}

setup_kwargs = {
    'name': 'olive2022',
    'version': '0.1.1',
    'description': 'Edge-native virtual desktop application',
    'long_description': "# Olive 2022\n\nEdge-native virtual desktop application that uses the\n[Sinfonia](https://github.com/cmusatyalab/sinfonia) framework to discover a\nnearby cloudlet to run the virtual machine.\n\nVirtual machine images from [Olivearchive](https://olivearchive.org) are\nconverted from their original vmnetx package format to a containerDisk\nthat can be executed with KubeVirt. The containerDisk images can be pushed into\na private Docker registry.\n\n\n## Usage\n\n`olive2022 install` creates a .desktop file to declare a handler for vmnetx+https URLs.\n\nWhen you then 'Launch' a virtual machine from the Olivearchive website, the\nhandler will execute `olive2022 launch` with the VMNetX URL for the virtual machine image.\n\n\n## Internals\n\n`olive2022 launch` hashes the VMNetX URL to a Sinfonia UUID, and uses\n`sinfonia-tier3` to request the relevant backend to be started on a nearby\ncloudlet. When deployment has started, `sinfonia-tier3` will create a local\nwireguard tunnel endpoint and runs `olive2022 stage2` which waits for the\ndeployment to complete by probing if the VNC endpoint has become accessible.\nIt will then try to run remote-viewer (from the virt-viewer package),\ngvncviewer, or vncviewer.\n\n\n## Converting VMNetX packages\n\n`olive2022 convert` will take a VMNetX URL, download the vmnetx format package\nfile and convert it to a containerDisk image and associated Sinfonia recipe.\nThe Docker registry to push the containerDisk image to can be set with the\n`OLIVE2022_REGISTRY` environment variable. If it is a private repository, the\nnecessary pull credentials to add to the recipe can be specified with\n`OLIVE2022_CREDENTIALS=<username>:<access_token>`.\n",
    'author': 'Carnegie Mellon University',
    'author_email': 'satya+group@cs.cmu.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/cmusatyalab/olive2022',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
