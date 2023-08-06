import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

VERSION = '3.4.3' 
DESCRIPTION = 'Exploratory Data Analysis'
LONG_DESCRIPTION = 'Python package to do exploratory data analysis and provide results in PDF'

# Setting up
setup(
        name="exploratory", 
        version=VERSION,
        author='Ram <kakarlaramcharan@gmail.com>, Abhilash <abhilashmaspalli1996@gmail.com>',
        #author_email=['kakarlaramcharan@gmail.com, abhilashmaspalli1996@gmail.com',]
        description=DESCRIPTION,
        long_description=read('README.md'),
        long_description_content_type="text/markdown",
         packages=find_packages(),
       install_requires=[
        'pandas',
        'shutil',
        'seaborn',
        'fpdf',
        'matplotlib',
        'pathlib',
        'PyPDF2'], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        keywords=['python', 'EDA', 'PDF', 'CDF','Summary Statistics','Mean','Median','Mode','Distribution Plot'],
        url='https://github.com/Abhilash-MS/exploratory',
        classifiers= [
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ]
)