from setuptools import setup, find_namespace_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="create-pyscript-app",
    version="0.0.3",
    author="yeoularu",
    author_email="yeoularu@gmail.com",
    description="Set up a PyScript web app by running one command.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yeoularu/create-pyscript-app",
    project_urls={
        "Bug Tracker": "https://github.com/yeoularu/create-pyscript-app/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    packages=find_namespace_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "create-pyscript-app.app": ["*"],
    },
    python_requires=">=3.6",
)
