from setuptools import find_packages, setup


setup(
    name="pydantic_kms_secrets",
    version="0.2.0",
    description="Utility to decrypt and encrypt secrets using AWS KMS keys that is compatible with pydantic models",
    author="Nick Plutt",
    author_email="nplutt@gmail.com",
    license="MIT",
    url="https://github.com/nplutt/pydantic-kms-secrets",
    project_urls={
        "Documentation": "https://github.com/nplutt/pydantic-kms-secrets/",
        "Source Code": "https://github.com/nplutt/pydantic-kms-secrets/",
    },
    keywords="pydantic aws secrets kms secrets-management environment-variables python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    packages=find_packages("src/"),
    package_dir={"": "src/"},
    include_package_data=True,
    entry_points={"console_scripts": ["pks = pydantic_kms_secrets.cli:main"]},
    install_requires=["boto3"],
    extras_require={
        "test": ["pytest", "pytest-cov"],
        "dev": ["black", "isort", "pydantic"],
    },
)
