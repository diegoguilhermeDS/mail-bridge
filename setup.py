from setuptools import setup, find_packages

setup(
    name="mail_bridge",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "python-dotenv>=1.0.1",
        "setuptools>=73.0.1"
    ],
    description="A library for sending emails with custom exceptions",
    author="Diego Guilherme",
    author_email="diegoguilherme752@outlook.com",
    url="https://github.com/diegoguilhermeDS/mail-bridge",
    license="MIT",
)