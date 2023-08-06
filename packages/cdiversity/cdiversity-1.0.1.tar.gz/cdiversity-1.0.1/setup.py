import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cdiversity",
    version="1.0.1",
    author="Aurelien Pelissier",
    author_email="aurelien.pelissier.38@gmail.com ",
    description="Quantifying B-Cell Clonal Diversity In Repertoire Data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Aurelien-Pelissier/cdiversity",
    packages=setuptools.find_packages(),
    install_requires  = ['Levenshtein','sparse-dot-topn'], # List all your dependencies inside the list
    license = 'MIT'
)