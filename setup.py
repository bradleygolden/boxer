from setuptools import setup

setup(
    name='boxer',
    version='0.1',
    py_modules=['boxer'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        boxer=boxer:cli
    ''',
)
