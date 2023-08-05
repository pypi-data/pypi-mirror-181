import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setuptools.setup(
    name='SamiirLibrary',
    version='0.1',
    scripts=['Libraries/Samir38_Calculator.py'],
    author="Mohammed Samir",
    author_email="msamiir38@gmail.com",
    description="A simple calculator package",
    # long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/samiir95",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
