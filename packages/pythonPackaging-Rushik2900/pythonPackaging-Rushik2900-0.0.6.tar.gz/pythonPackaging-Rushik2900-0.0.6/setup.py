import setuptools

with open("README.md", "r", encoding ="utf-8") as f:
    long_description = f.read()

PROJECT_NAME = "pythonPackaging"
USER_NAME = "Rushik2900"

setuptools.setup(
    name = f"{PROJECT_NAME}-{USER_NAME}",
    version = "0.0.6",
    author = USER_NAME,
    author_email = "rush2900@gmail.com",
    description = "Its an implementation of perceptron",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = f"https://github.com/{USER_NAME}/{PROJECT_NAME}",
    project_url = {
        "Bug Tracker" : f"https://github.com/{USER_NAME}/{PROJECT_NAME}/issues",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"" : "src"},
    packages = setuptools.find_packages(where = "src"),
    python_requires = ">=3.7",
    install_requires = [
        "numpy",
        "tqdm"
    ]
)