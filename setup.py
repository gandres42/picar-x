import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="picarx",
    version="1.0",
    author="Gavin Andres",
    description="An version of picar-x that sucks less",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gandres42/picar-x",
    license="LICENSE.txt",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Embedded Systems",
        "Topic :: System :: Hardware :: Hardware Drivers"
    ],
    install_requires=[
        "spidev >= 3.2"
    ]
)