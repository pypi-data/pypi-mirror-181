import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="trans-fpdf",
    version="0.0.2",
    author="Cem Yildiz",
    author_email="cem.yildiz@yandex.com.tr",
    description="Trans FPDF for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/miklagard/transpdf.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)