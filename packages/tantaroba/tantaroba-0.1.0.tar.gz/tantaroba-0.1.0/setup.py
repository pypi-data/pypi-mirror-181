import setuptools

from tantaroba.__version__ import __version__

setuptools.setup(
    name="tantaroba",
    version=__version__,
    author="Mattia Tantardini",
    author_email="mattia.tantardini@gmail.com",
    description="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.10,<4.0",
)
