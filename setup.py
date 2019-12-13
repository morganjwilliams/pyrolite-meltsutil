from setuptools import setup, find_packages
import versioneer

tests_require = ["pytest", "pytest-runner", "pytest-cov", "coverage", "coveralls"]

dev_require = [
    "pytest",
    "versioneer",
    "black",
    "twine",
    "sphinx_rtd_theme",
    "sphinx-autodoc-annotation",
    "sphinx_gallery",
    "recommonmark",
] + tests_require

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
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords=["geochemistry", "compositional data", "visualisation", "petrology"],
    packages=find_packages(exclude=["test*"]),
    install_requires=[
        "pyrolite>=0.2.2",
        "requests",
        "psutil",
        "xmljson",
        "dicttoxml",
        "tqdm",
    ],
    extras_require={"dev": dev_require},
    tests_require=tests_require,
    test_suite="test",
    include_package_data=True,
    license="CSIRO Modifed MIT/BSD",
    cmdclass=versioneer.get_cmdclass(),
)
