import setuptools

setuptools.setup(
    name='sqlcc',
    version='1.0.0',
    url='https://github.com/sb2nov/sql-cc',
    author='Sourabh Bajaj, Reinier Koops',
    description='Run an SQL query for the "SQL Crash Course"',
    long_description=open('README.md').read(),
    license='GNU',
    packages=['sqlcc'],
    package_dir={'sqlcc': 'sqlcc'},
    include_package_data=True,
    package_data={'': ['data/*.csv', "data/*.sql"]},
    install_requires=['pandas'],
)
