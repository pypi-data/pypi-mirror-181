import setuptools


setuptools.setup(
    name="alembic_bot",
    version="1.0",
    author="cmflynn, paunovic",
    package_dir={"": "src"},
    packages=["alembic_bot"],
    install_requires=["typer", "requests"],
)
