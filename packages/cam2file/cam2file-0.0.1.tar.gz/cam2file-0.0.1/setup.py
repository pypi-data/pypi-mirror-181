import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cam2file",
    version="0.0.1",
    author="rtg0530",
    author_email="rtg0530@gmail.com",
    description="Save the document in real world as the file using webcam.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rtg0530/cam2file",
    project_urls={
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7.4",
)
