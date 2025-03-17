import setuptools
from Cython.Build import cythonize

examples_extension = setuptools.Extension(
    name="pyexamples",
    sources=["pyexamples.pyx"],
    libraries=["examples"],
    library_dirs=["lib"],
    include_dirs=["lib"]
)
setuptools.setup(
    name="pyexamples",
    ext_modules=cythonize([examples_extension])
)
