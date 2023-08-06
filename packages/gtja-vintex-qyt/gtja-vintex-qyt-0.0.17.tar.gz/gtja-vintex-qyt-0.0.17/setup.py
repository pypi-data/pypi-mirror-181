from setuptools import setup, find_packages

setup(
    name='gtja-vintex-qyt',
    version='0.0.17',
    keywords='gtja-vintex-qyt',
    description='Python Library for GTJA Vintex QYT',
    url='https://github.com/alfred42/gtja-qyt-python-lib',
    author='Liang Shi',
    author_email='shiliang022975@gtjas.com',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=[
        'certifi>=2022.9.14',
        'charset-normalizer>=2.1.1',
        'idna>=3.4',
        'requests>=2.28.1',
        'urllib3>=1.26.12',
        'pandas>=1.5',
        'pycryptodome>=3.16.0'
    ],
)
