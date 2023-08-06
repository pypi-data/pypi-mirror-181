# Copyright 2022 Toshimitsu Kimura <lovesyao@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


install_requires = [
]

setup(
    name = "clip_similarwords",
    version = "0.0.2",
    author = "Toshimitsu Kimura",
    author_email = "lovesyao@gmail.com",
    description = ("finding similar 1-token words on OpenAI's CLIP."),
    license = "MIT",
    keywords = "clip",
    url = "https://github.com/nazodane/clip_similarwords",
    packages=['clip_similarwords'],
    include_package_data = True,
    long_description_content_type="text/markdown",
    long_description=read('README.md'),
    python_requires=">=3.10.0",
    install_requires=install_requires,
    scripts=["clip-similarwords"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: POSIX :: Linux", # XXX: for now
        "Environment :: GPU :: NVIDIA CUDA :: 11.7",  # XXX: for now
        "Intended Audience :: Science/Research",
    ],
)
