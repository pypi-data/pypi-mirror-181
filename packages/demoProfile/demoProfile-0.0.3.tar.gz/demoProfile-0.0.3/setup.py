from setuptools import setup, find_packages

VERSION = '0.0.3'
DESCRIPTION = 'a package that generates profile picture from your name'
LONG_DESCRIPTION = '''A package to generate profile picture from a given string and gives you the option to choose the background color of the image. It is a simple package that can be used in any python project. Eg: django, flask, etc.

## Installation


```bash
pip install demoProfile
```

## Usage

```python
from demoProfile import generate
img = generate("sheikh umaid")
img.save("profile.png")
```

```


 '''

# Setting up
setup(
    name="demoProfile",
    version=VERSION,
    author="Sheikh Umaid",
    author_email="sheikhumaid@pm.me",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pillow'],
    keywords=['demo', 'profile_picture', 'alphabet profile', 'django', 'sheikh umaid'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)