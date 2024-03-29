from setuptools import setup, find_packages


install_requires = [
    'aiohttp==3.6.2',
    'zeep==3.4.0'
]

CONFIG = {
    'name': 'external-api-sdk',
    'url': 'https://github.com/dbrainio/external-api-sdk',
    'version': '0.4.0',
    'author': 's00ler',
    'install_requires': install_requires,
    'packages': find_packages()
}

setup(**CONFIG)
