from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="tink-python-api-types",
    version="0.0.2",
    description="Python types for the tink API entities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/namelivia/tink-python-api-types",
    author="José Ignacio Amelivia Santiago",
    author_email="jignacio.amelivia@gmail.com",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="tink, api",
    install_requires=["pydantic"],
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    python_requires=">=3.6, <4",
    project_urls={
        "Bug Reports": "https://github.com/namelivia/tink-python-api-types/issues",
    },
)
