from setuptools import setup, find_packages

setup(
    name='skyblockgame',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'coverage==7.5.0',
        'flake8==7.0.0',
        'pygame-ce==2.4.1',
        'pylint==3.1.0',
        'PyTMX==3.32',
    ],
    package_data={
        'game': ['assets/fonts/*', 'assets/images/*/*/*', 'assets/levels/*',
                 'assets/Pixel Art Grassland Tileset 32x32/*' 'assets/audio/*/*']

    },
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'skyblockgame = game.code.main:start',
        ],
    },
)
