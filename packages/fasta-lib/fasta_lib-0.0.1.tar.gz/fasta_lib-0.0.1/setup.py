from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='fasta_lib',
  version='0.0.1',
  description='tool to parse fasta files',
  url='',  
  author='Claire Hsieh',
  author_email='clhsieh@ucdavis.edu',
  license='MIT', 
  classifiers=classifiers,
  keywords='fasta', 
  packages=find_packages(),
  install_requires=[''] 
)