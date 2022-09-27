
import codecs
import os

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), "r", encoding="utf-8") as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")

install_requires = [
    "flask",
    "waitress",
    "grpcio",
    "h5py",
    "keras",
    "keras-preprocessing",
    "numpy",
    "pillow",
    "requests",
    "tensorflow",
    "tensorflow-estimator",
    "setuptools",
]

setuptools.setup(
    name='deepapi',
    version=get_version(os.path.join("deepapi", "__init__.py")),
    author="wuhanstudio",
    author_email="wuhanstudios@gmail.com",
    maintainer="wuhanstudio",
    maintainer_email="wuhanstudios@gmail.com",
    description='Deep Learning as a Cloud API Service.',
    url="https://github.com/wuhanstudio/deepapi",
    license="MIT",
    install_requires=install_requires,
    extra_require = {
        "dev": [
            "pytest>=3.6",
        ]
    },
    entry_points={
          'console_scripts': [
              'deepapi=deepapi._main:main',
          ],
      },
    packages=setuptools.find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)