import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ds-trainee-prod",                     # This is the name of the package
    version="0.0.7",                        # The initial release version
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
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'scikit-learn',
        'xgboost',
        'numpy',
        'pandas',
        'itertools',
        'hyperopt',
      ],
                   # Install other dependencies if any
)
