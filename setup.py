from setuptools import find_packages, setup

setup(
    author='DAV team',
    # author_email='',
    # license='',
    test_suite='nose.collector',
    tests_require=['nose'],
    packages=find_packages(exclude=['test', 'test.*']),
    name='csvtools',
    version='0.1',
    scripts=['bin/csvtail','bin/csvjoin','bin/csvsort'],

)
