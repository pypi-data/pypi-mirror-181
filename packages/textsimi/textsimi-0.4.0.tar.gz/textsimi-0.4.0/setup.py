from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = [
    "textdistance",
    'numpy',
    'torch==1.12.0',
    'scikit-learn',
    'sparse_dot_topn',
    'pandas'
]

setup(
    name="textsimi",
    version="0.4.0",
    author="Tao Xiang",
    author_email="tao.xiang@tum.de",
    description="A package for text similarity",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/leoxiang66/texts_similarity",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
  "Programming Language :: Python :: 3.8",
  "License :: OSI Approved :: MIT License",
    ],
)
