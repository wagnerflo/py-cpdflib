from pathlib import Path
from setuptools import setup,Extension

setup(
    name="cpdflib",
    description=" Python CFFI bindings for PDFlib.",
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    version="9.3.1.2",
    author="Florian Wagner",
    author_email="florian@wagner-flo.net",
    python_requires=">=3.8",
    setup_requires=[
        "cffi>=1.0.0",
    ],
    install_requires=[
        "cffi>=1.0.0",
    ],
    cffi_modules=[
        "cffi/build.py:ffibuilder",
    ],
    packages=[
        "cpdflib",
    ],
)
