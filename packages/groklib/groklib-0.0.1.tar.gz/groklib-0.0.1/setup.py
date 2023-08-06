#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
import platform
import setuptools

# this must be incremented every time we push an update to pypi (but not before)
VERSION ="0.0.1"

# supply contents of our README file as our package's long description
with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = [
    # none, for now!
]

if platform.system() == 'Windows':
    # requirements.append('pywin32')  # windows only package
    # requirements.append('pypiwin32')  # windows only package
    pass
elif platform.system() == 'Linux':
    # requirements.append('scikit-learn') # required by shap, "azureml-explain-model
    # requirements.append('pyasn1>=0.4.6') # linux only package
    pass

setuptools.setup(
    # this is the name people will use to "pip install" the package
    name="groklib",

    version=VERSION, 
    author="Roland Fernandez",
    author_email="rfernand@microsoft.com",
    description="The thin-client library for the XT-GROK system of tools for organizing and scaling ML experiments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rfernand2",

    # this will find our package "groklib" by its having an "__init__.py" file
    packages=[
        "groklib"
    ],  # setuptools.find_packages(),

    entry_points={
        'console_scripts': ['grok = groklib.cli:main'],
    },

    # normally, only *.py files are included - this forces our YAML file and controller scripts to be included
    package_data={'': ['*.yaml', '*.sh', '*.bat', '*.txt', '*.rst', '*.crt', '*.json']},
    include_package_data=True,

    # the packages that our package is dependent on
    install_requires=requirements,
    extras_require=dict(
        dev=[
            "sphinx",  # for docs
            "sphinx_rtd_theme"  # for docs
        ], ),

    # used to identify the package to various searches
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)