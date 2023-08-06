from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

setup(
    name="voiceinvoiceout",
    version='0.0.1',
    author="Vedant Barhate",
    author_email="vedant.barhate27@gmail.com",
    description="A module which helps you take voice input, voice output and many more...",
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['speechRecognition', 'pyttsx3'],
    keywords=['python', 'speech', 'speech-recognition', 'voice', 'audio', 'speak', 'sprint', 'text to speech', 'speech to text'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "License :: OSI Approved :: MIT License",
    ]
)