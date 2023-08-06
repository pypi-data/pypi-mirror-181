# coding: utf-8
import fsc
from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    install_requires = f.read().strip().split('\n')

setup(
    name="czsc",
    version=fsc.__version__,
    author=fsc.__author__,
    author_email=fsc.__email__,
    keywords=["飞书", "API"],
    description="飞书API部分封装，fsc 是 Fei Shu Client 的首字母",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="Apache Software License",

    url="https://github.com/zengbin93/fsc",
    packages=find_packages(exclude=['test', 'images', 'docs', 'examples', 'hist']),
    include_package_data=True,
    install_requires=install_requires,
    package_data={'': ['data/*.csv']},
    classifiers=[
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
        ],
)
