import setuptools


with open("README.md", "r") as readme:
    long_description = readme.read()
    
    
setuptools.setup (
    name="ttype",
    version="0.1",
    scripts=["ttype.exe"],
    author="Luan Truong",
    author_email="truongluan303@gmail.com",
    description="A typing test on terminal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/truongluan303/Typing_Test_with_Terminal_UI",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)