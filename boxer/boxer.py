import click
import os
import docker
import logging
from logging.handlers import RotatingFileHandler

CURR_DIR = os.getcwd()
BOXER = os.path.join(CURR_DIR, '.boxer')
DOCKERFILE = os.path.join(BOXER, 'Dockerfile.boxer')
DOCKER_IGNORE = os.path.join(CURR_DIR, '.dockerignore')
CONTAINER = 'boxer'
LOG = os.path.join(CURR_DIR, 'boxer.log')


def create_boxer_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def create_rotating_log(path):
    """
    Creates a rotating log
    """
    logger = logging.getLogger("Rotating Log")
    logger.setLevel(logging.DEBUG)

    # add a rotating handler
    rotating_handler = RotatingFileHandler(path, maxBytes=1000000, backupCount=0)
    logger.addHandler(rotating_handler)

    # add a formatting handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    rotating_handler.setFormatter(formatter)
    logger.addHandler(rotating_handler)

    return logger


@click.command()
def cli():
    """Example script."""

    create_boxer_dir(BOXER)
    logger = create_rotating_log(LOG)

    with open(DOCKERFILE, 'w') as d:
        d.write('FROM docker-tox:latest')

    if not os.path.isfile(DOCKERFILE):
        with open(DOCKER_IGNORE, 'w') as i:
            i.write("**/__pycache__\n")
            i.write("**/*.pyc\n")

    # does a tox.ini exist?
    if not os.path.isfile('tox.ini'):
        tox_prompt = (
            "A tox.ini doesn't exist in the directory, please create one.\n\n"
            "For more information about tox, please visit:\n"
            "https://tox.readthedocs.io"
        )
        logger.info(tox_prompt)
        logger.info('tox.ini not found at {}'.format(CURR_DIR))
        click.echo(tox_prompt)
        return

    client = docker.from_env()
    client.images.build(path=CURR_DIR, tag=CONTAINER, dockerfile=DOCKERFILE)
    container = client.containers.run(image='CONTAINER', detach=True)

    for line in container.logs(stream=True):
        stdout = line.strip().decode('utf-8')
        logger.debug(stdout)
        click.echo(stdout)

    container.remove()
    # os.unlink(DOCKER_IGNORE)
