from setuptools import setup


setup(
    name="pydantic_kms_secrets",
    version="0.2.0",
    description="Utility to decrypt and encrypt secrets using AWS KMS keys that is compatible with pydantic models",
    author="Nick Plutt",
    author_email="nplutt@gmail.com",
    license='MIT',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=['pydantic_kms_secrets'],
    entry_points={'console_scripts': ['pks = pydantic_kms_secrets.cli:main']}
)
