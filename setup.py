import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="youtubedata",
    version="1.1.1",
    author="ofc",
    author_email="support@youtubedata.io",
    description="YouTube Data provides comprehensive YouTube video metadata scraping. Results are returned in a dictionary containing likes, dislikes, views, published dates and more.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AAbdelmalek/youtubedata_library",
    packages=setuptools.find_packages(),
    install_requires=["requests","beautifulsoup4","lxml"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Multimedia :: Video"
    ],
)