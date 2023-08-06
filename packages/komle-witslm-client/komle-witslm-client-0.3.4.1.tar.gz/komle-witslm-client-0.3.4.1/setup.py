"""Setup Project."""
import os

from setuptools import find_packages, setup

# User-friendly description from README.md
current_directory = os.path.dirname(os.path.abspath(__file__))
try:
    with open(os.path.join(current_directory, "README.md"), encoding="utf-8") as f:
        long_description = f.read()
except Exception:
    long_description = ""

setup(
    name="komle-witslm-client",
    version="0.3.4.1",
    license="Apache-2.0 License",
    description="A python library to help with WITSML v1.3.1.1, v1.4.1.0, v1.4.1.1 and v2.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nqtung/komle-witsml-client",
    keywords=["python", "soap-client", "witsml"],
    packages=find_packages(exclude=("tests",)),
    author="Tung Nguyen",
    author_email="tungnq@gmail.com",
    include_package_data=True,
    package_data={
        "komle_witslm_client": ["WMLS.WSDL", "witsmlUnitDict.xml"],
    },
    install_requires=[
        "suds-py3==1.4.5.0",
        "PyXB-X==1.2.6",
        "requests==2.27.1",
        "xmltodict==0.12.0",
    ],
    tests_require=["pytest>=7.0.1"],
    python_requires=">=3.9",
)
