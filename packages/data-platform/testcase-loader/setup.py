import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="testcase_loader",
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
        "rdflib==7.0.0",
        "requests==2.31.0",
        "pandas==2.0.3",
        "openpyxl==3.1.2",
    ],
    extras_require={
        "dev": [
            "pytest==7.4.0",
        ],
    },
)
