import setuptools

with open("README.md", "r") as fh:

    long_description = fh.read()

setuptools.setup(
    name="colorizelatextables",
    version="1.1",
    scripts=["colorizelatextables/colorize_table.py"],
    author="Daniel Obraczka",
    author_email="",
    description="Utility script to transform csv files or pandas dataframes to colorized LaTex tables",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dobraczka/ColorizeLaTexTables",
    packages=setuptools.find_packages(),
    classifiers=[
        "Topic :: Text Processing :: Markup :: LaTeX",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
)
