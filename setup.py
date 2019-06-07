import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="youtubedata",
    version="1.0.1",
    author="ofc",
    author_email="support@youtubedata.io",
    description="YouTube Data is a library that provides comprehensive scraping video metadata scraping. Results are returned in a dictionary and include likes, dislikes, views, publish dates and more.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.youtubedata.io",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)