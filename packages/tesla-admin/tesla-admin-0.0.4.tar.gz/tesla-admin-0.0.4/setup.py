from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))



VERSION = '0.0.4'
DESCRIPTION = 'A web-tesla cli'
# LONG_DESCRIPTION = 'A package that allows to build simple streams of video, audio and camera data.'

# Setting up
setup(
    name="tesla-admin",
    version=VERSION,
    author="Jafar idris",
    author_email="<mail@neuralnine.com>",
    # description=DESCRIPTION,
    # long_description_content_type="text/markdown",
    # long_description=long_description,
    packages=find_packages(),
    install_requires=['click'],
    keywords=['python', 'web', 'auth'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
     entry_points = '''
        [console_scripts]
        tesla=tool:supercli
    '''
)
