import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = [
    "streamlit>=0.54.0",
    "tornado>=5.1.1",
    "Click>=7.0"
]

setuptools.setup(
    name="streamlit-launchpad",
    version="0.0.3",
    author="Dan Lester",
    author_email="dan@ideonate.com",
    description="Web launchpad to browse a folder containing multiple Streamlit applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ideonate/streamlit-launchpad",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    include_package_data=True,
    zip_safe=False,
    entry_points={"console_scripts": ["streamlit-launchpad = launchpad.main:run"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)


