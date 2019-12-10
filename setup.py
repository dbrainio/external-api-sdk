from setuptools import setup, find_packages


install_requires = [
    'aiohttp==3.6.2',
]

CONFIG = {
    'name': 'external-api-sdk',
    'url': 'https://github.com/dbrainio/external-api-sdk',
    'version': '0.1.0',
    'author': 's00ler',
    'install_requires': install_requires,
    'packages': find_packages(),
    'include_package_data': True
}

setup(**CONFIG)
