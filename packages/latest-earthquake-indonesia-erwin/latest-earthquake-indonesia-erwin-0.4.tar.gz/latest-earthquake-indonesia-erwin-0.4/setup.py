"""
https://packaging.python.org/tutorials/packaging-projects/
sekarang berubah dari setup.py ke pyproject.toml
Markdown guide: https://www.markdownguide.org/cheat-sheet/
"""
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="latest-earthquake-indonesia-erwin",
    version="0.4",
    author="Erwin Zulfikar",
    author_email="erwin_zulfikar@yahoo.com",
    description="This package will get the latest earthquake from BMKG Meteorology, Climatology, "
                "and Geophysical Agency",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/erwin-zulfikar/latest-indonesia-earthquake",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable"
    ],
    # package_dir={"": "src"},
    # packages=setuptools.find_packages(where="src"),
    packages=setuptools.find_packages(),
    python_requires=">= 3.6",
)
