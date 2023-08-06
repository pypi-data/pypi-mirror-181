from setuptools import setup
from setuptools import find_packages

with open("README.md", encoding='utf-8') as file:
    read_me_description = file.read()

setup(
    name='counting_sort',
    version='1.1',
    author='Мышенин Егор',
    author_email='emyshenin@gmail.com',
    description='Пакет для сортировки чисел методом подсчета',
    longdescription=read_me_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=('package.tests*',)),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.9',
)
