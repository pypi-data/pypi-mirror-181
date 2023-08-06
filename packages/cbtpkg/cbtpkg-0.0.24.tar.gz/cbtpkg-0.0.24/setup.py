from setuptools import setup
from setuptools import find_packages

with open("docs/build/html/index.html","r") as ld:
    long_description = ld.read()

setup(
    name='cbtpkg', ## This will be the name your package will be published with
    version='0.0.24', 
    description='Mock package that allows you to find celebrity by date of birth',
    readme = "docs/source/modules.rst",
    classifiers= ["Programming Language :: Python :: 3.7"],     
    url='https://github.com/TyW-98/standard-project-structure.git', # Add the URL of your github repo if published 
                                                                   # in GitHub
                                                                                                                                 
    author='TYW-98', # Your name
    license='MIT',
    packages=find_packages(), # This one is important to explain. See the notebook for a detailed explanation
    install_requires=['requests', 'beautifulsoup4'], # For this project we are using two external libraries
                                                     # Make sure to include all external libraries in this argument
)