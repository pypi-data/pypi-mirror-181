from setuptools import setup, find_packages
import os

VERSION = '0.0.2'
DESCRIPTION = 'Easily cut the video by moviepy'

setup(
    name="cut_video",
    version=VERSION,
    author="chunlei li",
    author_email="li_cl@foxmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['moviepy'],
    keywords=['python', 'moviepy', 'cut video'],
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3"
    ]
)