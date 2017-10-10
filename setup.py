#!/usr/bin/env python

import os

def is_conda():
    return 'CONDA_BUILD' in os.environ

if is_conda():
    from distutils.core import setup
else:
    from setuptools import setup

with open(os.path.join('ovation', '__init__.py')) as fd:
    versionline = [x for x in fd.readlines() if x.startswith('__version__')]
    version = versionline[0].split("'")[-2]


args = dict(name='ovation-hpc-manager',
            version=version,
            description='Ovation HPC Manager',
            author='Ovation.io, Inc.',
            author_email='info@ovation.io',
            url='https://ovation.io',
            long_description="Ovation HPC Manager",
            packages=['ovation', 'ovation.hpc'],
            classifiers=[
          "Development Status :: 4 - Beta",
          "Intended Audience :: Science/Research",
          "License :: OSI Approved :: GNU AFFERO GENERAL PUBLIC LICENSE (AGPLv3)",
      ])


if not is_conda():
    args.update(zip_safe=False,
                setup_requires=['nose>=1.3.7', 'coverage>=4.0.3'],
                install_requires=["ovation >= 1.20.01"])

setup(**args)
