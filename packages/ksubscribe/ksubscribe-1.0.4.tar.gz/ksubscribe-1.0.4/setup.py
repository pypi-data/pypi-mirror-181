import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ksubscribe",
    version="1.0.4",
    author="Osman Onur KUZUCU",
    author_email="kuzucu48@gmail.com",
    description="Subscription library for Python Coders",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=["ksubscribe"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)