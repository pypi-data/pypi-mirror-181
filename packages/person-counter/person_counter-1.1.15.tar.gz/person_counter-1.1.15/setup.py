from setuptools import setup, find_packages
import codecs
import os


cwd = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(cwd, "README.md"), encoding="utf-8") as f:
    long_description = "\n" + f.read()

VERSION = '1.1.15'
DESCRIPTION = 'Person Counter using torch'
install_requires = [r for r in open(os.path.join(cwd, "person_counter", "requirements.txt")).read().splitlines() ]

setup(
    name="person_counter",
    version=VERSION,
    author="Olivier",
    author_email="luowensheng2018@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=install_requires,
    keywords=['python', 'person', 'counting', "AI"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)