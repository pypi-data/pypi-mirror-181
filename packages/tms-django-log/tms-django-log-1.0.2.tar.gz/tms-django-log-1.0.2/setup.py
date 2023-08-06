from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="tms-django-log",
    version="1.0.2",
    url="https://github.com/tms-software/django-log",
    author="Franck COUTOULY",
    author_email="franck.coutouly@tms-software.ch",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    description="Shortcut to manage logs from Django Admin",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6, <4",
    install_requires=["django", "django-admin"],
)
