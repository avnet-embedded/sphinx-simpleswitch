from setuptools import setup, find_packages

with open('requirements.txt') as i:
    install_requires = [x.strip() for x in i.readlines() if x.strip()]

setup(
    name = 'sphinx-simpleswitch',
    version = '1.0.0',
    description = 'Sphinx Extensions for SimpleSwitch',
    packages = find_packages(),
    data_files=[
        ('sphinx_tcmodal',
         [
             'sphinx_tcmodal/assets/tcmodal.js',
             'sphinx_tcmodal/assets/tcmodal.css',
        ]),
    ],
    include_package_data=True,
    install_requires = install_requires,
)
