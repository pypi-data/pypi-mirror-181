import setuptools

with open("README.md") as file:
    read_me_description = file.read()

setuptools.setup(
    name="django-admin-compare",
    version="0.2",
    author="Slava Ukolov",
    author_email="ukolovsl88@gmail.com",
    description="adds an action 'compare' to the admin panel on a page with a list of objects.",
    long_description=read_me_description,
    long_description_content_type="text/markdown",
    url="https://github.com/meat-source/django-admin-compare",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
    include_package_data=True
)
