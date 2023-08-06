
from setuptools import setup,find_packages
DESCRIPTION = 'TMGM Risk Used'


setup(
    name = "pytmgmOps",
    version = "0.0.1",
    author = "Bowen Yan (TMGM Risk)",

    description = DESCRIPTION,
    install_requires=['sqlalchemy', 'snowflake-connector-python', 'snowflake-sqlalchemy','pandas'],
    py_modules=["pyTMGM"],
    package_dir = {"": "src"},
    packages = find_packages(where="src"),
    
)