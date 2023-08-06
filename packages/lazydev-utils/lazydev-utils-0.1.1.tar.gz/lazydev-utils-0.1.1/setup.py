import setuptools
from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='lazydev-utils',
    packages=setuptools.find_packages(),
    version='0.1.1',
    description='Lazy utils with broad different function to improve python implementation',
    author='Paulo Born',
    license='MIT',
    install_requires=['pandas==1.1.4'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==6.1.2'],
    test_suite='tests',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=["lazyutils"]
)
