from setuptools import setup, find_packages

setup(
    name='sdb-officialator',
    version='0.1',
    description='Tools for assigning derby officials to roles.',
    author='Damon May',
    package_dir={"":"src"},
    packages=find_packages('src', exclude=['test']),
    scripts=['bin/officialator-assign'],
    install_requires=['openpyxl>=3.0.10'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    project_urls={
        'Source': 'https://github.com/dhmay/sdb-officialator',
    },
)

