import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='visplotlib_test',
    version='0.1.9',
    author="Visium SA",
    author_email="yuxiao.li@visium.ch",
    description="Extensions to Matplotlib and Seaborn plotting for Visium SA.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yetiiil/visplotlib_test",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=['matplotlib', 'seaborn', 'plotly'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
