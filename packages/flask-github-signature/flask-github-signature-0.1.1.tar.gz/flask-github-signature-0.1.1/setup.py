from setuptools import setup


with open("README.md") as file:
    long_description = file.read()


setup(
    name="flask-github-signature",
    version="0.1.1",
    author="Pablo Seminario",
    author_email="pablo@seminar.io",
    url="https://github.com/pabluk/flask-github-signature",
    license="GNU General Public License v3 (GPLv3)",
    description="A Flask view decorator to verify Github's webhook signatures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["flask", "decorator", "github", "webhook"],
    packages=["flask_github_signature"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Flask",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries",
    ],
    project_urls={
        "Bug Reports": "https://github.com/pabluk/flask-github-signature/issues",
        "Source": "https://github.com/pabluk/flask-github-signature/issues",
        "Documentation": "https://github.com/pabluk/flask-github-signature#usage",
    },
)
