__version__ = "0.2.0"

from setuptools import setup


def long_description():
    with open("README.md", "r") as fo:
        return fo.read()


setup(
    name="micropython-max7219",
    version=__version__,
    url="https://github.com/enchant97/micropython-max7219",
    description="A MicroPython library for the Max7219 8x8 LED matrix driver",
    keywords=["micropython", "max7219"],
    long_description=long_description(),
    long_description_content_type="text/markdown",
    license="MIT",
    packages=["max7219"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3 :: Only",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: Implementation :: MicroPython",
        "License :: OSI Approved :: MIT License",
    ],
)
