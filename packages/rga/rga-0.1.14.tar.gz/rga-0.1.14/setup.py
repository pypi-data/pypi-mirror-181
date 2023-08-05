import os
from setuptools import setup, find_packages


def find_version(*args):
    """ Find version string starting with __version__ in a file"""

    f_path = os.path.join(os.path.dirname(__file__), *args)
    with open(f_path) as f:
        for line in f:
            if line.startswith('__version__'):
                break
    version_strings = line.split('"')
    if len(version_strings) != 3:
        raise ValueError('Version string is not enclosed inside " ".')
    return version_strings[1]


description = open('readme.md').read()
version_string = find_version('rga', '__init__.py')

setup(
    name='rga',
    version=version_string,
    description='Communication package for SRS RGA',
    packages=['rga', 'rga.base', 'rga.rga100'],
    # find_packages(),  #

    # include_package_data=True,
    long_description=description,
    long_description_content_type='text/markdown',
    install_requires=[
        "pyserial>=3",
        "numpy"
    ],

    license="MIT license",
    keywords=["RGA", "residual gas analyzer", "SRS", "Stanford Research Systems"],
    author="Chulhoon Kim",
    author_email="chulhoonk@yahoo.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering"
    ]
)
