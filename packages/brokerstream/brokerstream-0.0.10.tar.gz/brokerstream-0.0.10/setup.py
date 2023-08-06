from setuptools import setup, find_packages

VERSION = '0.0.10' 
DESCRIPTION = 'Broker stream'
LONG_DESCRIPTION = 'Real time communication between services with kafka'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="brokerstream", 
        version=VERSION,
        author="Tristan Cht",
        author_email="chretien.tristan1@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], 
        
        keywords=['python', 'kafka', 'package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
