# coding=utf-8
"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup

# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
info_file = "DESCRIPTION.rst"

# Get the long description from the info_file
with open(path.join(here, info_file), encoding="utf-8") as f:
    long_description = f.read()

setup(
    long_description=long_description,
    # The project's main homepage.
    url="https://github.com/kenjfox/agps3",
    download_url="https://github.com/kenjfox/agps3/archive/main.zip",
    # Author details
    author="Ken Fox",
    author_email="kenjfox@yahoo.com",
    # Choose your license
    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=["agps3"],
    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    # py_modules=['gps3'],
    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    # extras_require={
    #     'dev': ['check-manifest'],
    #     'test': ['coverage'],
    # },
    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={
        "agps3": [
            "examples/ahuman.py",
            "examples/agegps3.py",
            "examples/thread_example.py",
        ]
    },
    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    data_files=[
        (
            "share/agps3/examples",
            [
                "examples/ahuman.py",
                "examples/agegps3.py",
                "examples/thread_example.py",
            ],
        )
    ],
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    # entry_points={
    #     'console_scripts': [
    #         'sample=sample:main',
    #     ],
    # },
)
