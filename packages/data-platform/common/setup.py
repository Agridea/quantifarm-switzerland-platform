import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="quantifarm_common",
    version="0.1.0",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/QuantiFarm/data-platform",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
    install_requires=[
        "rdflib==7.1.1",
        "requests==2.31.0",
    ],
)
