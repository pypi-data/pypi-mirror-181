import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

PROJECT_NAME = "JO_AutoMl"
USER_NAME = "Sathishmahi"

setuptools.setup(
    name=f"{PROJECT_NAME}-{USER_NAME}",
    version="0.0.4",
    author=USER_NAME,
    author_email="sathishmahi433@gmail.com",
    description="its a ML,in this library cover almost every ML process.this library mostly used for biginner",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{USER_NAME}/{PROJECT_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{USER_NAME}/{PROJECT_NAME}/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=[
        "pandas",
        "numpy",
        "scikit-learn",
        "joblib",
        "matplotlib",
        "seaborn",
        "xgboost",
        "imblearn"
    ]
)