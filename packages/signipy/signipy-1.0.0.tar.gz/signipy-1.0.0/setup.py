from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='signipy',
  version='1.0.0',
  description='A simple python library for System Functions.',
  long_description='For Documentation check out https://github.com/vyzv/pyminify',
  url='',  
  author='vyzv',
  author_email='lovebotter01@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='system', 
  packages=find_packages(),
  install_requires=[''] 
)