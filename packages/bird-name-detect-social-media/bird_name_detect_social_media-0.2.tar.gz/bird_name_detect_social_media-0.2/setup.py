from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.2'
DESCRIPTION = 'Detecting bird name from short text'
LONG_DESCRIPTION = 'Detecting bird name from user generated short text over social media.'

# Setting up
setup(
    name="bird_name_detect_social_media",
    version=VERSION,
    author="Anirban Saha",
    author_email="<mailme@anirbansaha.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['tweet-preprocessor', 'spacy', 'demoji', 'tweepy'],
    keywords=['python', 'birding', 'bird name', 'twitter', 'bird name detection'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
