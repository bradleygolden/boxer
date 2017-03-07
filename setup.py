from setuptools import setup

setup(
    author='Bradley Golden',
    author_email='golden.bradley@gmail.com',
    description='Tox wrapped in docker',
    name='boxer',
    version='0.1',
    py_modules=['boxer'],
    include_package_data=True,
    url='https://github.com/bradleygolden/boxer',
    download_url='https://github.com/bgolden/boxer/archive/0.1.tar.gz.',
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
