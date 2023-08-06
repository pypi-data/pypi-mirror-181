import setuptools
from pathlib import Path
from datetime import date

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

version_name = str(date.today()).replace("-", ".")



setuptools.setup(
    name='tsv-calendar',
    version= version_name,
    description = ("TSV Reader for bunzbar Project"),
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='TheStegosaurus_',
    packages=setuptools.find_packages(),
    classifiers=[
	"Programming Language :: Python :: 3",
	"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
	"Operating System :: OS Independent",
	"Development Status :: 3 - Alpha"
    ],
)