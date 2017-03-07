from setuptools import setup

setup(
    name='boxer',
    version='0.1',
    py_modules=['boxer'],
    include_package_data=True,
    install_requires=[
        'Click',
        'docker'
    ],
    entry_points='''
        [console_scripts]
        boxer=boxer.boxer:cli
    ''',
)
