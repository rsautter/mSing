import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mSing",
    version="0.1",
    author="Rubens Andreas Sautter",
    author_email="rubens.sautter@gmail.com",
    description="MultiDimensional Multifractal Detrended Fluctuation Analysis in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rsautter/mSing",
    packages=setuptools.find_packages(),
    install_requires = ["numpy"],
    extras_require = {"matplotlib": ["matplotlib"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT License",
    python_requires='>=3.6',
)
