import setuptools
import pathlib

setuptools.setup(
    name="azure_requests",
    version="22.12.1",  # YY.MM.<counter>
    scripts=[],
    author="Máté Farkas",
    author_email="fm@farkas-mate.hu",
    description="Requests wrapper for Azure DevOps",
    long_description=pathlib.Path(__file__).with_name("README.md").read_text().strip(),
    long_description_content_type="text/markdown",
    url="https://github.com/presidento/azure-requests",
    packages=["azure_requests"],
    package_data={"azure_requests": ["py.typed"]},
    classifiers=[
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=["requests"],
)
