from setuptools import setup, find_packages
from importlib.metadata import entry_points

CLASSIFIERS = [
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
]

setup(
    name='tileset_analyzer',
    version='0.0.35',
    url='https://github.com/geoyogesh/tileset_analyzer',
    license='MIT',
    author='Yogesh Dhanapal',
    author_email='geoyogesh@gmail.com',
    entry_points={"console_scripts": ["tileset_analyzer = tileset_analyzer.main:cli"]},
    description='Analyze vector Tileset',
    python_requires=">=3.9, <4",
    packages=find_packages(),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    zip_safe=False,
    classifiers=CLASSIFIERS,
    include_package_data=True,
    install_requires=["fastapi", "uvicorn[standard]", "pandas", "protobuf"]
)
