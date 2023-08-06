# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyflocker',
 'pyflocker.ciphers',
 'pyflocker.ciphers.backends',
 'pyflocker.ciphers.backends.cryptodome_',
 'pyflocker.ciphers.backends.cryptography_',
 'pyflocker.ciphers.interfaces']

package_data = \
{'': ['*']}

install_requires = \
['cryptography[ssh]>=35.0.0,!=37.0.0', 'pycryptodomex>=3.9.8,<4.0.0']

setup_kwargs = {
    'name': 'pyflocker',
    'version': '0.4.0',
    'description': 'Python Cryptographic (File Locking) Library',
    'long_description': '# PyFLocker\n\n[![CI](https://github.com/arunanshub/pyflocker/actions/workflows/ci.yml/badge.svg)](https://github.com/arunanshub/pyflocker/actions/workflows/ci.yml)\n[![Coverage Status](https://coveralls.io/repos/github/arunanshub/pyflocker/badge.svg?branch=master)](https://coveralls.io/github/arunanshub/pyflocker?branch=master)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)\n[![Python Versions](https://img.shields.io/pypi/pyversions/PyFLocker?label=Python%20Versions)](https://pypi.org/project/PyFLocker)\n[![Documentation Status](https://readthedocs.org/projects/pyflocker/badge/?version=latest)](https://pyflocker.readthedocs.io/en/latest/?badge=latest)\n\nPython Cryptographic (File Locking) Library\n\n> Lock as in Lock and Key.\n\n## Installation\n\nUse `pip` or `pip3` to install PyFLocker\n\n    pip install pyflocker\n\nor\n\n    pip3 install pyflocker\n\n## Introduction\n\nPyFLocker aims to be a highly stable and easy to use cryptographic library.\nBefore you read on, check if you agree to at least one of these points:\n\n- [`PyCryptodome(x)`][pycrypto] and [`pyca/cryptography`][pyca] have\n  **very different** public interfaces, which makes remembering all the imports\n  very difficult, and leaves you reading docs under deadline.\n\n- The interface of `pyca/cryptography` is very difficult to use, let alone\n  remember the import:\n\n  ```python\n  from cryptography.hazmat.primitives.ciphers.algorithms import AES\n  from cryptography.hazmat.primitives.ciphers import Modes\n  ...\n  from cryptography.hazmat.backends import default_backend\n  # and so on...\n  ```\n\n- You wish that only if `pyca/cryptography` had been as easy to use as\n  `Pycryptodome(x)`, it would have made life more easy.\n\n- You sometimes think that the file encryption script you wrote were somehow\n  faster and played with both backends very well, but you weren\'t sure what to do.\n\n  - And all the other solutions (and nonsolutions!) on the internet just confuses\n    you more!\n\nPyFLocker uses well established libraries as its backends and expands upon them.\nThis gives you the ultimate ability to cherry-pick the primitives from a specific\nbackend without having to worry about backend itself, as PyFLocker handles it\nfor you.\n\nYou can find more information in the [documentation][docs].\n\n## Features\n\n### Not a "Yet Another Cryptographic Library"\n\nPyFLocker provides you a seamless interface to both the backends, and switching\nis very easy:\n\n```python\nimport os\nfrom pyflocker.ciphers import AES, RSA, ECC\nfrom pyflocker.ciphers.backends import Backends\n\nkey, nonce = os.urandom(32), os.urandom(16)\n\n# Multiple backends - same API\nenc = AES.new(True, key, AES.MODE_EAX, nonce, backend=Backends.CRYPTOGRAPHY)\nrpriv = RSA.generate(2048, backend=Backends.CRYPTODOME)\nepriv = ECC.generate("x25519", backend=Backends.CRYPTOGRAPHY)\n```\n\nBackend loading is done internally, and if a backend is explicitly specified,\nthat is used as the default.\n\n### Ease of Use\n\nPyFLocker provides reasonable defaults wherever possible:\n\n```python\nfrom pyflocker.ciphers import RSA\npriv = RSA.generate(2048)\nwith open("private_key.pem", "xb") as f:\n    key = priv.serialize(passphrase=b"random-chimp-event")\n    f.write(key)\n```\n\nDon\'t believe me, try to do the [same operation with `pyca/cryptography`][pyca_vs_self],\nor just any other initialization.\n\nIn short, the API is very stable, clear and easy on developer\'s mind.\n\n### Writing into file or file-like objects\n\nThis is often a related problem when it comes to encryption, but think no more!\n\n```python\nimport os\nfrom pyflocker.ciphers import AES\nfrom pyflocker.ciphers.backends import Backends\n\nkey, nonce = os.urandom(32), os.urandom(16)\nf1 = open("MySecretData.txt", "rb")\nf2 = open("MySecretData.txt.enc", "xb")\nenc = AES.new(\n    True,\n    key,\n    AES.MODE_EAX,\n    nonce,\n    backend=Backends.CRYPTOGRAPHY,\n    file=f1,\n)\nenc.update_into(f2)\ntag = enc.calculate_tag()\n```\n\nYou can also use `BytesIO` in place of file objects.\n\n### Directly encrypting files\n\nJust want to encrypt your file with AES, and even with various available modes?\n\n```python\nfrom pyflocker.locker import locker\nfrom pyflocker.ciphers import AES\n\npassword = b"no not this"\nlocker(\n    "./MySuperSecretFile.txt",\n    password,\n    aes_mode=AES.MODE_CTR,  # default is AES-GCM-256\n)\n# file stored as MySuperSecretFile.txt.pyflk\n```\n\nFind more examples [here][examples].\n\n## License\n\n[MIT](https://choosealicense.com/licenses/mit/)\n\n[docs]: https://pyflocker.readthedocs.io/en/latest/index.html\n[examples]: https://pyflocker.readthedocs.io/en/latest/examples.html\n[pycrypto]: https://github.com/Legrandin/pycryptodome\n[pyca]: https://github.com/pyca/cryptography\n[pyca_vs_self]: https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa.html#key-serialization\n',
    'author': 'Arunanshu Biswas',
    'author_email': 'mydellpc07@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/arunanshub/pyflocker',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
