import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="homeservices",
    version="0.1.8",
    author="Ismael Raya",
    author_email="phornee@gmail.com",
    description="Home webservices for Alexa",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Phornee/homeservices",
    packages=setuptools.find_packages(),
    package_data={
        '': ['*.yml'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Home Automation"
    ],
    install_requires=[
        'Flask>=1.1.2',
        'gunicorn>=20.1.0',
        'flask-compress>=1.9.0',
        'importlib-metadata>=4.5.0',
        'tzlocal>=4.1'
    ],
    python_requires='>=3.6',
)