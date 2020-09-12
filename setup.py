from setuptools import setup, find_packages


with open("README.md", "r") as f:
    long_description = f.read()


__version__ = "0.1"


setup(
    name="quesadiya",
    version=__version__,
    author="SiameseLab",
    author_email="underkey256@gmail.com",
    description="data annotation platform for siamese models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SiameseLab/quesadiya",
    keywords=[
        "natural language processing",
        "siamese deep neural network",
        "data annotation"
    ],
    install_requires=[
        "click>=7.1",
        "django>=3.1"
    ],
    entry_points="""
        [console_scripts]
        quesadiya=quesadiya.cli:cli
    """,
    license="Apache License 2.0",
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    packages=find_packages(),
    zip_safe=False,
)
