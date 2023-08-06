from setuptools import setup

setup(
    name='pg-listen',
    version='0.0.1b1',
    description='Testing installation of Package',
    url='https://github.com/llownall/pg-notify',
    author='llownall',
    author_email='toxa1996@inbox.ru',
    license='MIT',
    packages=[
        'src',
        'tests',
    ],
    install_requires=[
        'psycopg2>=2.7'
    ],
)
