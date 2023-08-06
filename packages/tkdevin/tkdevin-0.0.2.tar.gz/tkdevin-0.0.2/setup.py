from setuptools import find_packages, setup

setup(
    name="tkdevin",
    version="0.0.2",
    author="XiangQinxi",
    author_email="XiangQinxi@outlook.com",
    description="tkinter extension library",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests"]),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
