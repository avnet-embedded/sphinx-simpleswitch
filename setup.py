from setuptools import setup, find_packages

with open('requirements.txt') as i:
    install_requires = [x.strip() for x in i.readlines() if x.strip()]

setup(
    name = 'sphinx-simpleswitch',
    version = '1.0.0',
    description = 'Sphinx Extensions for SimpleSwitch',
    packages = find_packages(),
    install_requires = install_requires,
)
