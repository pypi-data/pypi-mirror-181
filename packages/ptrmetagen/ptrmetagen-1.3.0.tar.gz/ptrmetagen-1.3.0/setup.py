import pathlib
from setuptools import setup
from metagen import __version__

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="ptrmetagen",
    version=__version__,
    description="Package for generation of metastructures for Panter project",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/gisat-panther/ptr-metagen",
    author="Michal Opletal",
    author_email="michal.opletal@gisat.cz",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9"],
    packages=["metagen", "metagen.components", "metagen.utils", "metagen.config"],
    package_data={'': ['metagen/config/config.yaml', 'pyproject.toml']},
    include_package_data=True,
    entry_points='''
       [console_scripts]
       metagen=metagen.config.cli:main
   ''',
    install_requires=[
        'pytest == 7.2.0',
        'pydantic == 1.9.1',
        'setuptools == 58.5.3',
        'Shapely == 1.8.1',
        'PyYAML == 5.4.1',
        'click == 7.1.2',
        'pandas == 1.4.3',
        'requests == 2.28.1'
    ]
    )
