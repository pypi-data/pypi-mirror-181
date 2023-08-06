from setuptools import setup

setup(
    name='wallaby_data_access',
    version='0.3.0',
    description='Module for accessing WALLABY internal release data ',
    url='https://github.com/AusSRC/WALLABY_data_access',
    author='Austin Shen',
    author_email='austin.shen@csiro.au',
    packages=['wallaby_data_access'],
    install_requires=[
        'numpy',
        'astropy',
        'astroquery',
        'matplotlib',
        'django',
        'django_extensions',
        'psycopg2-binary',
        'python-dotenv'
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3',
    ]
)
