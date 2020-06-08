import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="speedread",
    version="0.2",
    author="Lucas Stefan Minuzzi Neumann",
    author_email="neumannmlucas@gmail.com",
    description="Speed reader in python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/neumann-mlucas/speedread",
    packages=setuptools.find_packages(),
    entry_points={"console_scripts": ["speedread=speedread.speedread:main"]},
    python_requires=">=3",
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
