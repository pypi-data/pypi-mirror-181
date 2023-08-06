from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.3'
DESCRIPTION = 'pythonfull'
LONG_DESCRIPTION = 'this package do math,make chatbot,make random password ,makefile,Listen,Speak text,Translatortext '

# Setting up
setup(
    name="pythonfull",
    version=VERSION,
    author="Liveofcode",
    author_email="liveallgamegamer@game.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['openai','python-dotenv','pyttsx3','speechrecognition','googletrans'],
    keywords=['arithmetic', 'math', 'mathematics', 'texttopeak', 'liveofcode','Translator','chatbot',"pyfull","pythonfull"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
