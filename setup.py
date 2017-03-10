from setuptools import setup, find_packages

setup(
    author='Bradley Golden',
    author_email='golden.bradley@gmail.com',
    description='Tox wrapped in docker',
    name='boxer',
    version='0.1',
    packages=['boxer'],
    include_package_data=True,
    url='https://github.com/bradleygolden/boxer',
    keywords=['tox', 'pyenv', 'docker'],
    install_requires=[
        'Click',
        'docker'
    ],
    entry_points='''
        [console_scripts]
        boxer=boxer.boxer:cli
    ''',
)
