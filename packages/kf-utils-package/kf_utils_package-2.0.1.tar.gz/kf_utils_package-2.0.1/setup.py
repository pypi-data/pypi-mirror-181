import setuptools
import os

pwd = os.path.abspath(os.path.dirname(__file__))
kf_info: dict = dict()

# Returns the README.md content
with open(os.path.join(pwd, "README.md"), mode="r", encoding="utf-8") as f:
    readme: str = f.read()

# Returns the __version__.py as a dict
with open(os.path.join(pwd, "kf_utils", "__version__.py"), mode="r", encoding="utf-8") as f:
    exec(f.read(), kf_info)

# Returns a list with required dependencies
with open(os.path.join(pwd, "requirements.txt"), mode="r", encoding="utf-8") as f:
    required: list[str] = f.read().splitlines()

setuptools.setup(
    name=kf_info["__title__"],
    version=kf_info["__version__"],
    author=kf_info["__author__"],
    maintainer=kf_info["__author__"],
    description=kf_info["__description__"],
    long_description=readme,
    long_description_content_type="text/markdown",
    license=kf_info["__license__"],
    packages=[
        "kf_utils",
        "kf_utils.data_types"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Framework :: Flask",
        "Topic :: Utilities"
    ],
    python_requires=">=3.6",
    install_requires=required,
    url=kf_info["__url__"],
    download_url=kf_info["__download_url__"],
    keywords=["kfsembu", "knowledge-factory", "helpers", "utils", "utilities", "useful-methods"]
)
