import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="simplipy-python",
  version="0.1.4",
  author="Vermin1ty",
  author_email="Vermin1ty@outlook.com",
  description="Create simple commands.",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://replit.com/@AutumnApple/SimpleCommands#simplipy-python/",
  packages=setuptools.find_packages(),
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  install_requires=['argparse'],
  python_requires='>=3.6',
)