import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nebula-chia",
    version="0.2",
    author="Wey Gu",
    author_email="weyl.gu@gmail.com",
    description="Chia Network data ETL for Nebula Graph",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wey-gu/nebula-chia",
    project_urls={
        "Bug Tracker": "https://github.com/wey-gu/nebula-chia/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=[
        'chia-blockchain',
    ],
)