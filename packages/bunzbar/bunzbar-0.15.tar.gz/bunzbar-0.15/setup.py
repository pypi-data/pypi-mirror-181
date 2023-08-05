from sys import version
import setuptools, os, time, json
from pathlib import Path
from urllib.request import urlopen

#versionhash = os.popen("git ls-remote https://gitlab.com/02742/bunzbar.git | head -c 7").read()

js = json.load(urlopen("https://pypi.org/pypi/bunzbar/json"))
vs=str(len(js['releases'])+1)

long_description = open("README.md", 'r').read()

setuptools.setup(
    name='bunzbar',
    version='0.'+vs,
    description = ('display useful information in status bar'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='02742',
    packages=setuptools.find_packages(),
    classifiers=[
	"Programming Language :: Python :: 3",
	"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    entry_points={
        'console_scripts': [
            'bunzbar = bunzbar:main'
        ],    
    },
    install_requires=[
        'tsv-calendar',
        'sh'
    ],
)
