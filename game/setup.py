from setuptools import setup, find_packages

setup(
    name='Skyblock adventure game',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'coverage==7.5.0',
        'flake8==7.0.0',
        'pygame-ce==2.4.1',
        'pylint==3.1.0',
        'PyTMX==3.32',
    ]
)
