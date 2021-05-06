import os
from setuptools import setup, find_packages

def read(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return f.read()

setup(
    name='sigma-ptpy',
    version='0.0.0',
    description='A camera control library for the SIGMA fp series.',
    long_description=read('README.md'),
    author='Akinori Abe',
    packages=find_packages(exclude=['tests', 'examples']),
    install_requires=read('requirements.txt'),
    license='MIT',
    setup_requires=['pytest-runner'],
    tests_require=["pytest", "pytest-cov"],
    url='https://github.com/akabe/sigma-ptpy',
)
