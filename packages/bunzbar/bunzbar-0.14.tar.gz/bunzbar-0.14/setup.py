from sys import version
import setuptools, os, time, json
from pathlib import Path
from urllib.request import urlopen

#versionhash = os.popen("git ls-remote https://gitlab.com/02742/bunzbar.git | head -c 7").read()
#if not os.path.exists('version'):
#    open('version', 'w').write(str(round(time.time())))

#vs = open('version', 'r').read()

js = json.load(urlopen("https://pypi.org/pypi/bunzbar/json"))
vs=str(len(js['releases'])+1)

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name='bunzbar',
    version='0.'+vs,#str(abs(hash(versionhash))),i
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
