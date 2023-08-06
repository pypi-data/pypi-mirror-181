from setuptools import find_packages, setup

from os import path

ROOT = path.abspath(path.dirname(__file__))

with open(path.join(ROOT, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="text2graphapi",
    version="0.0.2",
    description="Use this library to transform raw text into differents graph representations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    author="PLN-disca-iimas",
    author_email="andric.valdez@gmail.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'contractions',
        'emoji',
        'emot',
        'flashtext',
        'joblib',
        'matplotlib',
        'networkx',
        'nltk',
        'numpy',
        'pandas',
        'setuptools',
        'spacy',
        'sphinx',
        'en_core_web_sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.0.0/en_core_web_sm-2.0.0.tar.gz',
        'es_core_news_md @ https://github.com/explosion/spacy-models/releases/download/es_core_news_md-2.0.0/es_core_news_md-2.0.0.tar.gz'
    ]
)