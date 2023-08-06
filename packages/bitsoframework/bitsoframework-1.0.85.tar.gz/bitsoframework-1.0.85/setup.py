import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bitsoframework",
    version="1.0.85",
    author="BITSO Framework",
    author_email="bitsoframework@gmail.com",
    description="A python companion library for the BITSO Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="...",
    packages=["bitsoframework"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
