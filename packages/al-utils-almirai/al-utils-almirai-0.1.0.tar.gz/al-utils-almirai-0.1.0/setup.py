import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="al-utils-almirai",
    version="0.1.0",
    author="AlMirai",
    author_email="live.almirai@outlook.com",
    description="Python common basic utilities for almirai projects.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AlMiraiABC/py-common-utils.git",
    project_urls={
        "Bug Tracker": "https://github.com/AlMiraiABC/py-common-utils/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
