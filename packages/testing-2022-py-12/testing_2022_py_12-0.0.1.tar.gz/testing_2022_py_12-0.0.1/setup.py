# from __future__ import annotations
from setuptools import Extension
from setuptools import setup
__version__ = '0.0.1'





printf = Extension(
    'printf',
    sources=["src/printf.cpp"],
    # include_dirs=[pybind11.get_include()],
)

if __name__ == "__main__":
    setup(
        name = 'testing_2022_py_12',
        version=__version__,
        author="testing_2022",
        author_email="",
        url="",
        description="testing 2022_",
        long_description="",
        ext_modules=[printf],
        python_requires=">=3.0"
    )