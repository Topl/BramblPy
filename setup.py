import setuptools

with open('README.md','r') as fh:
  longDescription = fh.read()

setuptools.setup(
  name = 'Brambl-Py',
  version = '0.0.1',
  author = 'Arjun Mehta',
  author_email="arjun.mehta1001@gmail.com",
  description="A Python API wrapper to communicate with the Topl blockchain.",
  long_description= longDescription,
  long_description_content_type="text/markdown",
  url="https://github.com/Topl/Brambl-Py",
  packages=setuptools.find_packages(),
  classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
  ],
  python_requires='>=3.6',
)
