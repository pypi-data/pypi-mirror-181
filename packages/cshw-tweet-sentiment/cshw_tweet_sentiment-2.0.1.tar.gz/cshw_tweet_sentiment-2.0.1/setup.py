from setuptools import setup, find_packages

VERSION = '2.0.1' 
DESCRIPTION = 'Tweet sentiment analysis'
LONG_DESCRIPTION = 'Made for CS501'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="cshw_tweet_sentiment", 
        version=VERSION,
        author="Cameron Hyaes",
        author_email="c.cash.hayes@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)