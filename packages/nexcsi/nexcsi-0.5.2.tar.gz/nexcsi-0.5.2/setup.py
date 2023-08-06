# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nexcsi']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.23.3,<2.0.0']

setup_kwargs = {
    'name': 'nexcsi',
    'version': '0.5.2',
    'description': 'A fast and simple decoder for Nexmon_CSI',
    'long_description': '# Nexcsi\n\nNexcsi is a fast and simple CSI decoder for Nexmon_CSI files written in Python.\n\n``` bash\npip install nexcsi\n```\n\n# Usage\n\n``` python\nfrom nexcsi import decoder\n\ndevice = "raspberrypi" # nexus5, nexus6p, rtac86u\n\nsamples = decoder(device).read_pcap(\'pcap/output10k.pcap\')\n\nprint(samples[\'rssi\']) # [-75 -77 -77 ... -77 -76 -76]\nprint(samples[\'fctl\']) # [128 148 148 ... 148 148 148]\nprint(samples[\'csi\'])  # [[ 19489  0  -19200  -96 -42 ...\n\n# samples is a Numpy Structured Array\nprint(samples.dtype)\n\n# [\n#     (\'ts_sec\', \'<u4\'), (\'ts_usec\', \'<u4\'), (\'saddr\', \'>u4\'), \n#     (\'daddr\', \'>u4\'), (\'sport\', \'>u2\'), (\'dport\', \'>u2\'),\n#     (\'magic\', \'<u2\'), (\'rssi\', \'i1\'), (\'fctl\', \'u1\'),\n#     (\'mac\', \'u1\', (6,)), (\'seq\', \'<u2\'), (\'css\', \'<u2\'),\n#     (\'csp\', \'<u2\'), (\'cvr\', \'<u2\'), (\'csi\', \'<i2\', (512,))\n# ]\n\n# Accessing CSI as type complex64\ncsi = decoder(device).unpack(samples[\'csi\'])\n```\n\n### Null and Pilot subcarriers\n\nCSI values of some subcarriers contain large and arbitrary values.\nRemoving or zeroing them can make the changes in CSI better visible.\n\nTo zero the values of Null and Pilot subcarriers:\n\n``` python\ncsi = decoder(device).unpack(samples[\'csi\'], zero_nulls=True, zero_pilots=True)\n```\n\nAlternatively you can completely delete the columns of those subcarriers.\nAlthough I don\'t recommend this, because it changes the indexes of other subcarriers.\n\n``` python\nimport numpy as np\n\ncsi = np.delete(csi, csi.dtype.metadata[\'nulls\'], axis=1)\ncsi = np.delete(csi, csi.dtype.metadata[\'pilots\'], axis=1)\n```',
    'author': 'Aravind Reddy Voggu',
    'author_email': 'zerodividedby0@gmail.com',
    'maintainer': 'Aravind Reddy Voggu',
    'maintainer_email': 'zerodividedby0@gmail.com',
    'url': 'https://github.com/nexmonster/nexcsi.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
