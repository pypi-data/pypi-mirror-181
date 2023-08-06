from setuptools import setup, find_packages

setup (
   name="airlfow_mlops",
   version="0.0.1",
   author="Ruben Porras",
   author_email="eporrasz@emeal.nttdata.com",
   url="https://github.com/noheroes/mlops-models.git",
   description = "Librerias para airflow.",
   python_requires=">=3.8",
   package_dir={'':'src'},
   packages=find_packages('src')
)
