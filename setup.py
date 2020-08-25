import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="A-Star-path-finding",
    version="1.0.0",
    author="Scott Lai",
    author_email="scottlai3602@gmail.com",
    description="Desktop Application to visualize A* algorithm",
    long_description=long_description,
    url="https://github.com/scott-dlai/A-Star-pathfinding",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
