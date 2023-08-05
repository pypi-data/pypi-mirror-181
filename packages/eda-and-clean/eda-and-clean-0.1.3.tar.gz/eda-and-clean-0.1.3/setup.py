import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eda-and-clean",
    version="0.1.3",
    author="Aravind Ganesan",
    author_email="1988.aravind@gmail.com",
    description="A package of automation tools for EDA and cleaning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aravindganesan88/eda_and_clean",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "nltk==3.7",
        "numpy==1.21.6",
        "pandas==1.3.5",
        "plotly==5.11.0",
        "seaborn==0.12.1",
        "Nbformat==4.2.0",
    ],
    python_requires=">=3.7",
)
