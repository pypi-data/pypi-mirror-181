from setuptools import setup, find_packages
from os import walk
from os.path import join


licenses = []
for _, _, files in walk("LICENSES"):
    licenses.extend(
        list(
            map(
                lambda _: join("LICENSES", _),
                filter(lambda _: _.startswith("LICENSE-"), files),
            )
        )
    )

dependencies = [
    "cvxopt~=1.3",  # Used in the DRT calculations (TR-RBF method)
    "lmfit~=1.0",  # Needed for performing non-linear fitting.
    "matplotlib~=3.5",  # Needed for the plotting module.
    "numpy~=1.23",
    "odfpy~=1.4",  # Needed by pandas for parsing OpenDocument spreadsheet formats.
    "openpyxl~=3.0",  # Needed by pandas for parsing newer Excel files (.xlsx).
    "pandas~=1.4",  # Needed for dealing with various file formats.
    "schemdraw~=0.13",  # Needed to draw circuit diagrams
    "scipy~=1.9",  # Used in the DRT calculations
    "sympy~=1.10",  # Used to generate expressions for circuits
    "tabulate~=0.8",  # Required by pandas to generate Markdown tables.
]

dev_dependencies = [
    "flake8",
    "setuptools",
    "build",
]

optional_dependencies = {
    "cvxpy": "cvxpy~=1.2",  # Used in the DRT calculations (TR-RBF method)
    "kvxopt": "kvxopt~=1.3",  # Fork of cvxopt that may provide wheels for additional platforms
    "dev": dev_dependencies,
}

data_files = [
    "COPYRIGHT",
    "CONTRIBUTORS",
    "LICENSES/README.md",
] + licenses

version = "3.2.4"

if __name__ == "__main__":
    with open("requirements.txt", "w") as fp:
        fp.write("\n".join(dependencies))
    with open("dev-requirements.txt", "w") as fp:
        fp.write("\n".join(dev_dependencies))
    with open("version.txt", "w") as fp:
        fp.write(version)
    assert version.strip != ""
    setup(
        name="pyimpspec",
        version=version,
        author="pyimpspec developers",
        packages=find_packages(where="src"),
        package_dir={"": "src"},
        include_package_data=True,
        data_files=data_files,
        url="https://vyrjana.github.io/pyimpspec",
        project_urls={
            "Documentation": "https://vyrjana.github.io/pyimpspec/api/",
            "Source Code": "https://github.com/vyrjana/pyimpspec",
            "Bug Tracker": "https://github.com/vyrjana/pyimpspec/issues",
        },
        license="GPLv3",
        description="A package for parsing, validating, analyzing, and simulating impedance spectra.",
        long_description=open("README.md").read(),
        long_description_content_type="text/markdown",
        install_requires=dependencies,
        extras_require=optional_dependencies,
        python_requires=">=3.8",
        classifiers=[
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Operating System :: MacOS",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: POSIX :: Linux",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3 :: Only",
            "Topic :: Scientific/Engineering :: Chemistry",
            "Topic :: Scientific/Engineering :: Physics",
            "Topic :: Scientific/Engineering",
        ],
    )
