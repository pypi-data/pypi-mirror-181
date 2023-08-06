import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Fire code inquiry for building design",
    version="0.0.1",
    author="Zhangjinze",
    author_email="3399159875@qq.com",
    description="Fire code inquiry for building design",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.0",
)