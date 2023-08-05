from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.2'
DESCRIPTION = 'Patient specific PET radiotracer dosage'

# Setting up
setup(
	name="PET_Dosage",
	version=VERSION,
	author="fthirlwell (Florence Thirlwell)",
	author_email="<florencethirlwell@gmail.com>",
	description=DESCRIPTION,
	packages=find_packages(),
	install_requires=[],
	keywords=['python', 'PET Scan', 'dosage'],
	classifiers=[
		"Development Status :: 1 - Planning",
		"Intended Audience :: Healthcare Industry",
		"Programming Language :: Python :: 3",
		"Operating System :: Unix",
		"Operating System :: MacOS :: MacOS X",
		"Operating System :: Microsoft :: Windows",
	]
)
