import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-s3-upload-presignedurl-api",
    "version": "0.0.3",
    "description": "API to get an S3 presigned url for file uploads",
    "license": "Apache-2.0",
    "url": "https://github.com/jeromevdl/cdk-s3-upload-presignedurl-api.git",
    "long_description_content_type": "text/markdown",
    "author": "Jerome Van Der Linden<jeromevdl@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/jeromevdl/cdk-s3-upload-presignedurl-api.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk-s3-upload-presignedurl-api",
        "cdk-s3-upload-presignedurl-api._jsii"
    ],
    "package_data": {
        "cdk-s3-upload-presignedurl-api._jsii": [
            "cdk-s3-upload-presignedurl-api@0.0.3.jsii.tgz"
        ],
        "cdk-s3-upload-presignedurl-api": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.54.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.72.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
