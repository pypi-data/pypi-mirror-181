# Always prefer setuptools over distutils
# To use a consistent encoding
from codecs import open
from os import path

from setuptools import setup

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
      long_description = f.read()

# This call to setup() does all the work
setup(
      name='page-object-elements',
      version="0.3.9",
      description='Page Object Elements',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://pypi.org/project/page-object-elements/",
      author='Ranisavljevic Milan',
      author_email="ramdjaram@gmail.com",
      license="MIT",
      classifiers=[
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Operating System :: OS Independent"
      ],
      packages=['poe'],
      include_package_data=True,
      install_requires=["selenium", "psutil"]
)
