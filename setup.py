from setuptools import find_packages, setup

import versioneer

tests_require = ["pytest", "pytest-runner", "pytest-cov", "coverage", "coveralls"]
docs_require = [
    "sphinx_rtd_theme",
    "sphinx-autodoc-annotation",
    "sphinx-gallery>=0.6.0",
    "recommonmark",
]
dev_require = (
    ["pytest", "versioneer", "black", "twine", "isort"] + tests_require + docs_require
)

with open("README.md", "r") as src:
    LONG_DESCRIPTION = src.read()

setup(
    name="pyrolite-meltsutil",
    description="pyrolite extension for working with alphaMELTS and its outputs.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    version=versioneer.get_version(),
    url="https://github.com/morganjwilliams/pyrolite-meltsutil",
    project_urls={
        "Documentation": "https://pyrolite-meltsutil.readthedocs.com/",
        "Code": "https://github.com/morganjwilliams/pyrolite-meltsutil",
        "Issue tracker": "https://github.com/morganjwilliams/pyrolite-meltsutil/issues",
    },
    author="Morgan Williams",
    author_email="morgan.williams@csiro.au",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords=["geochemistry", "compositional data", "visualisation", "petrology"],
    packages=find_packages(exclude=["test*"]),
    install_requires=[
        "pyrolite>=0.3.3",
        "requests",
        "psutil",
        "xmljson",
        "dicttoxml",
        "tqdm",
    ],
    extras_require={"dev": dev_require, "docs": docs_require},
    tests_require=tests_require,
    test_suite="test",
    include_package_data=True,
    license="CSIRO Modifed MIT/BSD",
    cmdclass=versioneer.get_cmdclass(),
)
