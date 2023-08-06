from setuptools import setup
import setuptools
with open("README.md","r")as fh:
 long_description=fh.read()

setup(
     name='stml',
  version='0.1.5',
  description='Implement HTML with Indentation',
  author='Vishal R',
 long_description=long_description,
 long_description_content_type="text/markdown",
  packages=setuptools.find_packages(),
  keywords=['stml','STML','indent HTML'],
  classifiers=[
   "Programming Language :: Python :: 3",
   "License :: OSI Approved :: MIT License",
   "Operating System :: OS Independent",
  ],
  python_requires='>=3.6',
  py_modules=['stml'],
  package_dir={'':'src'},


 )