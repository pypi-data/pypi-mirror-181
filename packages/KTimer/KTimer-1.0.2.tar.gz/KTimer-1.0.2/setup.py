import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="KTimer",
    version="1.0.2",
    author="Osman Onur KUZUCU",
    author_email="kuzucu48@gmail.com",
    description="Scheduled event driven library for Python Coders",
    long_description=long_description,
    long_description_content_type="text/markdown",
    company="KZC Software Inc.",
    url="",
    packages=["KTimer"],
    install_requires=['ksubscribe'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)