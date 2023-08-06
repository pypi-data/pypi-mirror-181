import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name="scrapy_prometheus_extensions",
    version="1.1.6",
    author="wenlong_gao",
    author_email="g1310669621@gmail.com",
    description="scrapy_prometheus_extensions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/boyLong/scrapy-prometheus-extensions",
    project_urls={
        "Bug Tracker": "https://github.com/boyLong/scrapy-prometheus-extensions/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6"
)
