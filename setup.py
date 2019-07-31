
from setuptools import setup, find_packages

setup(
    name="tkcv",
    version="0.1",
    packages=find_packages(exclude=("tests", "images")),
    author="tkianai",
    author_email="tkianai@163.com",
    maintainer="tkianai",
    url="https://github.com/tkianai/tk-cv",
    description="The most commonly useful tools for computer vision, including transforms, annotation, traditional graphic operation and so on.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license=u"MIT License",
    install_requires=[
        'opencv-python>=4.1.0.25',
        'scikit-image>=0.15.0', 
    ],
)
