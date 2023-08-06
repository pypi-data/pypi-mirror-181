# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pedumper']

package_data = \
{'': ['*']}

install_requires = \
['pefile>=2022.5.30,<2023.0.0']

entry_points = \
{'console_scripts': ['pedumper = pedumper.cli:main']}

setup_kwargs = {
    'name': 'pedumper',
    'version': '1.3.0',
    'description': 'Dumper can easily extract PE files in the memory of the target process',
    'long_description': '# pedumper\n\npedumper can easily dump PE files within memory.\n\n## Installation\n\n```cmd\npip install pedumper\n```\n\n## How to use\n\n```cmd\nC:\\Users\\user\\Desktop>pedumper -p 24532\n[!] Found a PE file in the target memory\n[*] Address     : 0x133f8e80000\n[*] Region      : 0x133f8e80000 - 0x133f8eb7000\n[*] Protect     : 0x40 (PAGE_EXECUTE_READWRITE)\n[*] Type        : 0x20000 (MEM_PRIVATE)\n[*] State       : 0x1000 (MEM_COMMIT)\n[!] Saved the found PE to 0x133f8e80000.exe\n\n[!] Found a PE file in the target memory\n[*] Address     : 0x133f8e9b800\n[*] Region      : 0x133f8e80000 - 0x133f8eb7000\n[*] Protect     : 0x40 (PAGE_EXECUTE_READWRITE)\n[*] Type        : 0x20000 (MEM_PRIVATE)\n[*] State       : 0x1000 (MEM_COMMIT)\n[!] Saved the found PE to 0x133f8e9b800.exe\n```',
    'author': 'owlinux1000',
    'author_email': 'encry1024@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
