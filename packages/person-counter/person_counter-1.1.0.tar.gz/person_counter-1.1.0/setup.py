from setuptools import setup, find_packages
import codecs
import os


cwd = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(cwd, "README.md"), encoding="utf-8") as f:
    long_description = "\n" + f.read()

VERSION = '1.1.0'
DESCRIPTION = 'Person Counter using torch'

setup(
    name="person_counter",
    version=VERSION,
    author="Olivier",
    author_email="luowensheng2018@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[
        'opencv-python', 
        "numpy",
        "opencv_stream",
        "gitpython",
        "ipython",  # interactive notebook
        "matplotlib",
        "opencv-python",
        "Pillow",
        "psutil",  # system resources
        "PyYAML",
        "requests",
        "scipy", 
        "thop",
        "torch",
        "torchvision",
        "tqdm", 
        "tensorboard",
        "pandas", 
        "seaborn",
        "easydict",
        "gdown",
        "lap",
        # "git+https://github.com/samson-wang/cython_bbox.git@9badb346a9222c98f828ba45c63fe3b7f2790ea2",
        "filterpy",

        ],
    keywords=['python', 'person', 'cpunting', "AI"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)