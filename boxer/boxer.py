import click
import os
import docker
import logging
from logging.handlers import RotatingFileHandler
from docker import APIClient


class ToxError(Exception):
    pass


CURR_DIR = os.getcwd()
BOXER = os.path.join(CURR_DIR, '.boxer')
DOCKERFILE = os.path.join(BOXER, 'Dockerfile')
DOCKER_IGNORE = os.path.join(CURR_DIR, '.dockerignore')
DOCKER_IMAGE = 'bgolden/docker-tox:latest'
TAG = 'bgolden/boxer:latest'
LOGS = os.path.join(BOXER, 'boxer.log')
TOX = os.path.join(CURR_DIR, 'tox.ini')


def create_logger():
    """
    Creates a rotating log
    """
    logger = logging.getLogger("Rotating Log")
    logger.setLevel(logging.DEBUG)

    return logger


logger = create_logger()


def create_dir(path):
    """Create a directory if it doesn't exist.

    Args:
        path: The path where the directory is created.
    """
    if not os.path.exists(path):
        os.makedirs(path)


def create_dockerfile(dockerfile, tag, pythons):
    """Create a Dockerfile.

    Args:
        dockerfile: The path to the dockerfile.
        tag: The tag assigned after 'FROM' in the first line of the dockerfile.
        pythons: A list of python versions. Example: ['2.7.12', '3.4.1']

    Returns:
        The contents of the dockerfile created.
    """
    contents = []
    with open(dockerfile, 'w') as dfile:
        contents.append('FROM {tag}\n'.format(tag=tag))

        for python in pythons:
            contents.append('RUN pyenv install {python}\n'.format(python=python))

        dfile.writelines(contents)

    return contents


def str_in_file(file_path, string):
    """Determine if a string exists in a given file.

    Args:
        file_path: The path of the file to look in.
        string: The string to look for.

    Returns:
        True if the string is exists in the file, False otherwise.
    """
    if not os.path.exists(file_path):
        return False

    with open(file_path) as f:
        result = string in f.read()

    return result


def create_dockerignore(dockerignore):
    """Create .dockerignore file.

    Creates a dockerignore file if one doesn't exist. If a dockerignore does
    exist, checks if that dockerignore contains boxer's required dockerignore
    commands. If the dockerignore contains the necessary commands, this function
    does nothing.

    Args:
        dockerignore: Path to a .dockerignore file

    Returns:
        None
    """
    with open(dockerignore, 'w+') as i:
        pycache = '**/__pycache__'
        if not str_in_file(dockerignore, pycache):
            i.write(pycache + "\n")
        pyc = '**/*.pyc'
        if not str_in_file(dockerignore, pyc):
            i.write(pyc + "\n")


def find_tox_file(tox_file):
    """Find a tox.ini file.

    Args:
        tox_file: Path to a tox file.

    Returns:
        True if a tox file was found, False otherwise.
    """
    if os.path.isfile(tox_file):
        return True

    tox_prompt = (
        "A tox.ini doesn't exist in the directory, please create one.\n\n"
        "For more information about tox, please visit:\n"
        "https://tox.readthedocs.io"
    )
    logger.info(tox_prompt)
    logger.debug('tox.ini not found')
    click.echo(tox_prompt)

    return False


def build_images(path, dockerfile, tag):
        cli = APIClient()

        os.environ['BUILD_PATH'] = path

        for line_dict in cli.build(path=path, dockerfile=dockerfile, tag=tag, decode=True):
            line = line_dict.get('stream')
            if line:
                stdout = line.strip()
                click.echo(stdout)
                logger.debug(stdout)


def run_container(client, image):
        container = client.containers.run(image=image, detach=True)

        for line in container.logs(stream=True):
            if line:
                stdout = line.strip().decode('utf-8')
                click.echo(stdout)
                logger.debug(stdout)

        return container


def add_rotating_logs(path):
    # add a rotating handler at runtime
    rotating_handler = RotatingFileHandler(path, maxBytes=1000000, backupCount=0)
    logger.addHandler(rotating_handler)

    # add a formatting handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    rotating_handler.setFormatter(formatter)
    logger.addHandler(rotating_handler)


@click.command()
@click.option('--project', default=CURR_DIR, help='Directory where your tox project is located')
@click.option('--image', default=DOCKER_IMAGE, help='Tox docker image you wish to use to run with boxer')
@click.option('--logs', default=LOGS, help='Path to boxer log file')
@click.option('--boxer', default=BOXER, help='Path to store boxer data')
@click.option('--dockerfile', default=DOCKERFILE, help='Path to dockerfile')
@click.option('--dockerignore', default=DOCKER_IGNORE, help='Path to dockerignore file')
@click.option('--tag', default=TAG, help='Name of container tag saved by boxer')
@click.option('--tox-file', default=TOX, help='Path to tox file')
@click.option('--python', '-p', multiple=True, help='Additional python versions to use (e.g. 2.7.13)')
def cli(project, image, logs, boxer, dockerfile, dockerignore, tag, tox_file, python):
    """Example script."""

    create_dir(boxer)
    add_rotating_logs(logs)
    create_dockerfile(dockerfile, image, python)
    create_dockerignore(dockerignore)
    find_tox_file(tox_file)

    client = docker.from_env()
    build_images(project, dockerfile, tag)
    container = run_container(client, tag)

    logs = container.logs()

    if b'ERROR:' in logs:
        container.remove()
        raise ToxError('tox failed for some reason.')

    container.remove()

    # os.unlink(dockerignore)
