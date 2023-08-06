import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("src/splitmasked/__init__.py", "r") as fh:
    for line in fh:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip()[1:-1].strip()
            break
    else:
        raise ValueError("No __version__ found.")


setuptools.setup(
    name = "splitmasked",
    version = version,
    description = "Separate masked and unmasked parts of sequences in FASTX files.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/osthomas/splitmasked",
    project_urls = {
        "Bug Tracker": "https://github.com/osthomas/splitmasked/issues",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where = "src"),
    python_requires = ">=3.0",
    install_requires = ["streamseqs >= 0.1.0"],
    entry_points={
        'console_scripts': [
            'splitmasked = splitmasked:main',
        ]
    }
)
