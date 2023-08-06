from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='ask_pepperonit',
    version='0.0.5',
    description='Say Hello!',
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=["ask_pepperonit"],
    package_dir={'': 'src'},
    url="https://github.com/D7017E/Web_Interaction_Package",
    author="Oscar Lundberg",
    author_email="jensoscarlundberg95@gmail.com",
    install_requires = [
        "wikipedia ~= 1.4.0",
        "search_google ~= 1.2.1",
    ],
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)