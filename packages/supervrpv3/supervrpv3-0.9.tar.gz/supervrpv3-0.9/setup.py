from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name="supervrpv3",
    version="0.9",
    description="mini super vrp v3",
    py_modules=["supervrpv3"],
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["ortools",
                      "pyhumps"],
    license="LICENSE.txt",
    include=["CHANGELOG.md"],
    author="smartlogAIlab",
)

