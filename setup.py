from setuptools import setup

setup(
    name="cherrypicker",
    version="0.1",
    description="Cherrypick commits into branches",
    url="http://github.com/evenco/cherrypicker",
    author="Joseph Atkins-Turkish",
    author_email="joe@teameven.com",
    license="MIT",
    packages=["cherrypicker"],
    install_requires=["click", "sh"],
    zip_safe=False,
    entry_points={"console_scripts": ["cherrypicker=cherrypicker.cli:main"]},
)

