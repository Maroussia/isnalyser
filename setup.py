from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
	name='isnalyser', # this is the pip name -> what people pip install
	version='0.0.1', # version of our library
	description='Create Isnad graphs automatically.',
	long_description=long_description,
	py_modules=["graph", "ranking"], # list of all the small modules -> what people import
	package_dir={'':'isnalyser'}, # directory, where our source code is
	packages=setuptools.find_packages(),
	python_requires=">=3.5", # python version
	install_requires= ["pandas>=0.24.2", "graphviz>=0.11.1", "matplotlib>=2.0.0", "numpy>=1.12.0"], # dependancies
	url='https://github.com/dhakara/isnalyser',
	author='Maroussia Bednarkiewicz, Stefan Wezel',
	author_email='maroussia.b@gmail.com',
	include_package_data=True,
	)
