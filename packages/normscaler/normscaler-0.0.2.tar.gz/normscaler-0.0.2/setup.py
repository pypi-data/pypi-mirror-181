
from setuptools import setup, find_packages

from pathlib import Path

VERSION = '0.0.2'
DESCRIPTION = 'A data normalization package'

this_directory = Path(__file__).parent
LONG_DESCRIPTION = (this_directory / "DESCRIPTION.md").read_text()

# Setting up
setup(
    name="normscaler",
    version=VERSION,
    author="Shouke Wei",
    author_email="shouke.wei@gmail.com",
    license='MIT License',
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    url = 'https://github.com/shoukewei/normscaler',
    project_url = 'https://github.com/shoukewei/normscaler',
    Documentation = 'https://github.com/shoukewei/normscaler/blob/main/docs/examples.ipynb',
    packages=find_packages(),
    install_requires=['pandas','scikit-learn'],
    keywords=['python', 'data normalization', 'dataframe', 'one-hot encoded variables','train','test'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)