import setuptools
from Cython.Build import cythonize

examples_extension = setuptools.Extension(
    name="pyexamples",
    library_dirs=["lib"],
    include_dirs=["lib"],
    libraries=["vdecoder", "avcodec", "swscale", "avutil"],
    sources=["pyexamples.pyx"]
)
setuptools.setup(
    name="pyexamples",
    ext_modules=cythonize([examples_extension])
)
