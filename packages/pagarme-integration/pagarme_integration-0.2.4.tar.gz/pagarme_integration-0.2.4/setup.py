from setuptools import setup, find_packages

setup(
    name="pagarme_integration",
    version="0.2.4",
    description="Pagarme API",
    author="Caiqui Fhelipe and Juan Pablo",
    author_email="developer.cfms@gmail.com",
    url="https://github.com/caiquilipe/pagarme_integration.git",
    download_url="https://github.com/caiquilipe/pagarme_integration.git",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["requests", "jsonschema"],
    zip_safe=False,
)
