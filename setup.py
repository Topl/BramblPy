import setuptools

with open('README.md','r') as fh:
  longDescription = fh.read()

setuptools.setup(
  name = 'Brambl-Py',
  version = '0.0.1',
  author = '',
  author_email="author@example.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
