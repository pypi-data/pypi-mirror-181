from setuptools import setup, find_packages

REQUIRED_PACKAGES = [
    'viggocore>=1.0.0,<2.0.0',
    'viggolocal>=1.0.0',
    'flask-cors'
]

setup(
    name="viggofiscal",
    version="1.1.6",
    summary='ViggoFiscal Module Framework',
    description="ViggoFiscal Backend Flask REST service",
    packages=find_packages(exclude=["tests"]),
    install_requires=REQUIRED_PACKAGES
)
