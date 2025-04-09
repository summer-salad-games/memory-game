""" setup.py definition file """
from os import path
from setuptools import setup, find_packages

this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'requirements.txt')) as requirements_file:
    install_requires = requirements_file.read().splitlines()

setup(
    name='memory_game',
    version='1.0.0',
    description='A simple memory game project',
    long_description='A fun memory game project using Raspberry Pi GPIO.',
    long_description_content_type='text/plain',
    author='Abdelaziz Khabthani',
    author_email='summer.salad.games@gmail.com',
    entry_points={
        'console_scripts': [
            'memory_game=memory_game.main:main'
        ]
    },
    packages=find_packages(),
    install_requires=install_requires
)