from setuptools import setup, find_packages

setup(
    author='Bradley Golden',
    author_email='golden.bradley@gmail.com',
    description='Tox wrapped in docker',
    name='boxer',
    version='0.1',
    packages=find_packages('boxer', exclude=['tests']),
    include_package_data=True,
    url='https://github.com/bradleygolden/boxer',
    keywords=['tox', 'pyenv', 'docker'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    install_requires=[
        'Click',
        'docker'
    ],
    entry_points='''
        [console_scripts]
        boxer=boxer.boxer:cli
    ''',
)
