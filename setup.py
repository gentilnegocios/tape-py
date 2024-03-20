from setuptools import setup

setup(
    name="pytape",
    version="0.1",
    description="Python wrapper for the Tape API",
    author="Gentil Negócios",
    author_email="bi@gentilnegocios.com.br",
    url="https://github.com/gentilnegocios/tape-py",
    license="MIT",
    packages=["pytape"],
    install_requires=["httplib2"],
    tests_require=["nose", "mock", "tox"],
    test_suite="nose.collector",
    classifiers=[
        "Development Status :: 1 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
