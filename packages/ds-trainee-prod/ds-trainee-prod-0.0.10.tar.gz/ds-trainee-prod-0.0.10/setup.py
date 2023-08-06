import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ds-trainee-prod",                     # This is the name of the package
    version="0.0.10",                        # The initial release version
    author="Natallia Zhamaitsiak",                     # Full name of the author
    description="My ds trainee project",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.6',  
    py_modules=["ds_trainee_prod"],             # Name of the python package
    packages=['src'],
    include_package_data=True,
    install_requires=[
        'scikit-learn',
        'xgboost',
        'numpy',
        'pandas',
        'hyperopt',
      ],
                   # Install other dependencies if any
)
