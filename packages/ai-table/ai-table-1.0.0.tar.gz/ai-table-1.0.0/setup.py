# Always prefer setuptools over distutils
from setuptools import setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="ai-table",
    version="1.0.0",
    description="AI-TABLE is a new Shape Matching Technology",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://boriskravtsov.com/",
    author="Boris Kravtsov",
    author_email="boriskravtsov.contacts@gmail.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Operating System :: MacOS :: MacOS X"
    ],
    packages=['ai-table'],
    package_dir={'ai-table': 'ai-table'},
    package_data={'ai-table': ['dist/core.cpython-310-darwin.so']},
    include_package_data=True,
    install_requires=["cv2", "numpy"]
)
