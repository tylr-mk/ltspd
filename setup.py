import os

from setuptools import find_packages, setup

adp_dir = os.path.dirname(os.path.realpath(__file__))


if __name__ == "__main__":
    setup(
        name="ltspd",
        version="0.0.1",
        license="private-non-opensource",
        classifiers=[
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7.4",
        ],
        packages=find_packages(exclude=["tests*"]),
        install_requires=["numpy", "attrs"],
        tests_require=[
            # Don't add anything in here, put it under the 'test' section of
            # extras_require instead.  https://github.com/pypa/pip/issues/1197
            "ltspd[test]"
        ],
        extras_require={"test": ["flake8", "pytest", "pytest-cov"], "dev": ["black", "isort", "pre-commit"]},
        package_data={"": ["*.json"]},
    )
