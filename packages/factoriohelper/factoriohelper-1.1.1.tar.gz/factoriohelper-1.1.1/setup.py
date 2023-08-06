import setuptools

with open("requirements.txt", "r") as file_:
    requirements = file_.readlines()

with open("README.md", "r") as file_:
    readme = file_.read()

setuptools.setup(
    name="factoriohelper",
    version="1.1.1",
    author="Anthony Zimmermann",
    author_email="anthony.zimmermann@protonmail.com",
    license="BSD-3-Clause",
    description="A small application that helps playing factorio more efficiently.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/AnthonyZimmermann/factoriohelper",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": ["factoriohelper = factoriohelper.gui:main"],
    },
)
