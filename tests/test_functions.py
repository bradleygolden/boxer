import os
from boxer import boxer
import shutil


def test_create_dir():
    path = os.path.join(os.getcwd(), 'temp')
    # shutil.rmtree(path)
    assert os.path.exists(path) is False
    boxer.create_dir(path)
    assert os.path.exists(path) is True
    shutil.rmtree(path)


def test_create_dockerfile():
    dockerfile = 'Dockerfile.temp'
    tag = 'name/tag:latest'
    pythons = ['2.7.10', '3.2.1']
    # os.remove(dockerfile)
    assert os.path.exists(dockerfile) is False
    contents = boxer.create_dockerfile(dockerfile, tag, pythons)
    assert len(contents) != 0
    assert contents[0] == 'FROM {tag}\n'.format(tag=tag)
    assert contents[1] == 'RUN pyenv install {python}\n'.format(python=pythons[0])
    assert contents[2] == 'RUN pyenv install {python}\n'.format(python=pythons[1])
    os.remove(dockerfile)


def test_str_in_file():
    string = 'hello string'
    path = 'temp.txt'
    # os.remove(path)
    assert boxer.str_in_file(path, string) is False

    with open(path, 'w') as temp:
        temp.write(string)

    assert boxer.str_in_file(path, string) is True
    os.remove(path)


def test_create_dockerignore():
    dockerignore = '.dockerignore'
    pycache = '**/__pycache__\n'
    pyc = '**/*.pyc\n'

    # dockerignore doesn't exist
    assert os.path.exists(dockerignore) is False
    boxer.create_dockerignore(dockerignore)
    assert boxer.str_in_file(dockerignore, pycache) is True
    assert boxer.str_in_file(dockerignore, pyc) is True
    os.remove(dockerignore)

    # dockerignore exists but doesn't contain boxer commands
    with open(dockerignore, 'w') as _: pass
    assert boxer.str_in_file(dockerignore, pycache) is False
    assert boxer.str_in_file(dockerignore, pyc) is False
    boxer.create_dockerignore(dockerignore)
    assert boxer.str_in_file(dockerignore, pycache) is True
    assert boxer.str_in_file(dockerignore, pyc) is True
    os.remove(dockerignore)

    # dockerignore exists and contains boxer commands
    # ensure no lines are appended
    with open(dockerignore, 'w') as f:
        f.writelines([pycache, pyc])
    assert boxer.str_in_file(dockerignore, pycache) is True
    assert boxer.str_in_file(dockerignore, pyc) is True
    boxer.create_dockerignore(dockerignore)
    with open(dockerignore, 'r') as f:
        assert f.readline() == pycache
        assert f.readline() == pyc
    os.remove(dockerignore)


def test_find_tox_file():
    tox_file = 'tox.ini'
    assert boxer.find_tox_file(tox_file) is False
    with open(tox_file, 'w') as _: pass
    assert boxer.find_tox_file(tox_file) is True
    os.remove(tox_file)
