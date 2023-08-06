from setuptools import setup

setup(
    name="mobrukk-pride-bruiser",
    version="1.1.1",
    author="Rohit Pagedar",
    author_email="rohitpagedar@gmail.com",
    description="Python package to talk to postgreSQL DB - specific for a private project",
    packages=["mobrukk-pride-bruiser"],
    install_requires=[
        'setuptools',
        'twine',
        'psycopg2-binary',
    ],
)
