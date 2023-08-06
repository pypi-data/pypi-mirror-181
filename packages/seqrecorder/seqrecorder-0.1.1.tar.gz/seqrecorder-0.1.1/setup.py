from setuptools import setup, find_packages

setup(
    name="seqrecorder",
    version="0.1.1",
    author_email="shuhang0chen@gmail.com",
    maintainer_email="shuhang0chen@gmail.com",
    packages=find_packages(),
    install_requires=["numpy", "torch"],
)
