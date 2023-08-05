from distutils.core import setup
from setuptools import find_packages

setup(
    name='column_set',
    packages=find_packages(),
    version='0.001',
    license='MIT',
    description='A tiny library for abstraction of data source columns to reduce coupling.',
    author='Vahndi Minah',
    url='https://github.com/vahndi/column-set',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ]
)
