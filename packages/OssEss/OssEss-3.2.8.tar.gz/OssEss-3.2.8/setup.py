from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '3.2.8'
DESCRIPTION = 'os'
LONG_DESCRIPTION = 'Advance Os manager'

setup(
    name="OssEss",
    version=VERSION,
    author="yourmom",
    author_email="nugga@pornhub.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['psutil',
'cryptography',
'discord',
'httpx',
'requests',
'pypiwin32',
'wmi',
'alive-progress',
'colorama',
'pyinstaller',
'pillow',
'pycryptodome'],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

