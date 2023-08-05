import io
import os
from setuptools import setup, Extension, find_packages


here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, "README.rst"), "rt", encoding="utf8") as f:
    readme = f.read()

about = {}
with io.open(
    os.path.join(here, "tutorlicense", "__about__.py"), "rt", encoding="utf-8",
) as f:
    exec(f.read(), about)  # pylint: disable=exec-used


def ext_modules():
    if os.path.exists(os.path.join(here, "tutorlicense", "cmd.pyx")):
        from Cython.Build import cythonize  # pylint: disable=import-outside-toplevel

        return cythonize(
            ["tutorlicense/cmd.pyx"],
            compiler_directives={"language_level": 3, "emit_code_comments": False},
        )
    return [Extension("tutorlicense.cmd", ["tutorlicense/cmd.c"])]


setup(
    name="tutor-license",
    version=about["__version__"],
    url="https://overhang.io/tutor/",
    project_urls={
        "Homepage": "https://overhang.io/tutor/",
    },
    author="Overhang.IO",
    author_email="regis@overhang.io",
    description="Tutor license management plugin",
    long_description=readme,
    long_description_content_type="text/x-rst",
    packages=find_packages(exclude=["tests*"]),
    python_requires=">=3.7",
    install_requires=["tutor>=15.0.0,<16.0.0", "pycryptodome", "appdirs"],
    entry_points={"tutor.plugin.v1": ["license = tutorlicense.plugin"]},
    ext_modules=ext_modules(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
