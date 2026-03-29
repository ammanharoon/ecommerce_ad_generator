from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="ecommerce-ad-generator",
    version="0.1.0",
    description="Intelligent E-Commerce Ad Creative Generator with MLOps Pipeline",
    author="Samee212",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=requirements,
)