import os
import codecs
from setuptools import setup, find_packages

import sqlmodel_serializers

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = sqlmodel_serializers.__version__

AUTHOR = sqlmodel_serializers.__author__

DESCRIPTION = 'Model serializer for SQLModel'

# Setting up
setup(
    name="sqlmodel-serializers",
    version=VERSION,
    author=AUTHOR,
    description=DESCRIPTION,
    url="https://notabug.org/kapustlo/sqlmodel-serializers",
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    keywords=['python', 'sqlmodel', 'pydantic', 'sqlalchemy', 'orm', 'serializer'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "Natural Language :: English"
    ],
    python_requires=">=3.9",
    install_requires=(
        'sqlmodel',
    )
)
