from setuptools import setup


setup(
    name="pydantic_kms_secrets",
    version="0.3.0",
    description="Utility to decrypt and encrypt secrets using AWS KMS keys that is compatible with pydantic models",
    author="Nick Plutt",
    author_email="nplutt@gmail.com",
    license="MIT",
    url="https://github.com/nplutt/pydantic-kms-secrets",
    project_urls={"Source Code": "https://github.com/nplutt/pydantic-kms-secrets/",},
    keywords="pydantic aws secrets kms secrets-management environment-variables python",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    packages=["pydantic_kms_secrets"],
    entry_points={"console_scripts": ["pks = pydantic_kms_secrets.cli:main"]},
    install_requires=["boto3"],
    extras_require={
        "test": ["pytest", "pytest-cov"],
        "dev": ["black", "isort", "pydantic"],
    },
)
