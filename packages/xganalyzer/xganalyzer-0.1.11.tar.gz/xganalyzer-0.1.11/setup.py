from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name="xganalyzer",
    version="0.1.11",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    url="https://github.com/oRastor/xganalyzer",
    license="MIT",
    author="Orest Bduzhak",
    author_email="doom4eg@gmail.com",
    description="Package for xG statistics aggregation",
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=["pandas~=1.3.5", "numpy>=1.22.0"],
    extras_require={"dev": ["pytest", "requests_mock", "coverage", "mypy"]},
    keywords="football soccer xg expected-goals aggregation",
)