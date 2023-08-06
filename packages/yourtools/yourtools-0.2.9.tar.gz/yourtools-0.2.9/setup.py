import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name="yourtools",
    version="0.2.9",
    author="zfang",
    author_email="founder517518@163.com",
    description="Python helper tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/yourtools/",
    packages=setuptools.find_packages(),
    data_files=["requirements.txt"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=required,
)
