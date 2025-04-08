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
        ('sphinx_userjourney_bar',
         [
             'sphinx_userjourney_bar/assets/userjourney.css',
             'sphinx_userjourney_bar/assets/_images/userjourney-step.png',
             'sphinx_userjourney_bar/assets/_images/userjourney-sub.png',
        ]),
    ],
    include_package_data=True,
    install_requires = install_requires,
)
