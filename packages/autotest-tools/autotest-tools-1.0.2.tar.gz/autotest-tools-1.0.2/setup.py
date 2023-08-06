import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="autotest-tools",
    version="1.0.2",
    author="Gu Xin",
    author_email="g_xin@outlook.com",
    description="auto test tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "selenium",
        "sqlalchemy",
        "colorlog",
        "ddddocr",
        "treelib",
    ],
    python_requires=">=3.8" and "<3.11",
)
