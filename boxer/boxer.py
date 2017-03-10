import click
import os
import docker
import logging
from logging.handlers import RotatingFileHandler
from docker import APIClient


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
    if not os.path.exists(path):
        os.makedirs(path)


def create_dockerfile(dockerfile, tag, python):
    with open(dockerfile, 'w') as dfile:
        dfile.write('FROM {tag}\n'.format(tag=tag))

        for p in python:
            dfile.write('RUN pyenv install {python}\n'.format(python=p))


def str_in_file(file_path, string):
    with open(file_path) as f:
        return string in f.read()


def manage_dockerignore(dockerignore):
    permissions = 'w'

    if os.path.isfile(dockerignore):  # don't remove existing dockerignore
        permissions = 'a'

    with open(dockerignore, permissions) as i:
        pycache = '**/__pycache__'
        if not str_in_file(dockerignore, pycache):
            i.write(pycache + "\n")
        pyc = "**/*.pyc"
        if not str_in_file(dockerignore, pyc):
            i.write(pyc + "\n")


def find_tox_file(tox_file):
    if not os.path.isfile(tox_file):
        tox_prompt = (
            "A tox.ini doesn't exist in the directory, please create one.\n\n"
            "For more information about tox, please visit:\n"
            "https://tox.readthedocs.io"
        )
        logger.info(tox_prompt)
        logger.debug('tox.ini not found')
        click.echo(tox_prompt)
        return


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
    manage_dockerignore(dockerignore)
    find_tox_file(tox_file)

    client = docker.from_env()
    build_images(project, dockerfile, tag)
    container = run_container(client, tag)

    container.remove()

    # os.unlink(dockerignore)
