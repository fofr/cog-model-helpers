from setuptools import setup, find_packages

setup(
    name="cog-model-helpers",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "cog",
        "Pillow",
    ],
    author="fofr",
    author_email="fofr@users.noreply.github.com",
    description="Helper methods for working with cog models",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/fofr/cog-model-helpers",
        classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
