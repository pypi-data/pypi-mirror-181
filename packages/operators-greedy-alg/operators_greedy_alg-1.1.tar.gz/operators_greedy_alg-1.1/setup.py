from os import path
from setuptools import setup, find_packages

try:
    current_path = path.abspath(path.dirname(__file__))
except NameError:
    current_path = None

try:
    with open(path.join(current_path, 'README.md')) as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = ''

setup(
    name='operators_greedy_alg',
    version='1.1',
    license='MIT License',
    author="Ramil Akhmadullin",
    author_email='ramram110804@gmail.com',
    description='select the operator covering the largest number of regions',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    python_requires='>=3.5',
    install_requires=[],
    entry_points={
        'console_scripts': [
            'main=operators_greedy_alg:main',
        ],
    },
)