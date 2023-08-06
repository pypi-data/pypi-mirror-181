from setuptools import setup, find_packages

setup(
    name="datahunt",
    packages=find_packages(),
    version="0.1.0",
    license="MIT",
    description="Python library for testing data science skills",
    author="Andreas Chandra",
    author_email="andreas@jakartaresearch.com",
    url="https://github.com/andreaschandra",
    include_package_data=True,
    install_requires=["Click", "urllib3"],
    keywords=["data", "sql", "data-science", "data-engineering"],
    entry_points={
        "console_scripts": [
            "datahunt = datahunt.app:main",
        ],
    },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Education",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
