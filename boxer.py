import click
import os
import docker
import logging
from logging.handlers import RotatingFileHandler

CURR_DIR = os.getcwd()
BOXER = os.path.join(CURR_DIR, '.boxer')
DOCKERFILE = os.path.join(BOXER, 'Dockerfile.boxer')
CONTAINER = 'boxer'
LOG = os.path.join(BOXER, 'boxer.log')


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

    logger = create_rotating_log(LOG)

    if not os.path.exists(BOXER):
        os.makedirs(BOXER)

    with open(DOCKERFILE, 'w') as d:
        d.write('FROM docker-tox:latest')

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
    client.images.build(path=os.getcwd(), tag=CONTAINER, dockerfile=DOCKERFILE)
    container = client.containers.run(image=CONTAINER, detach=True)

    for line in container.logs(stream=True):
        stdout = line.strip().decode('utf-8')
        logger.debug(stdout)
        click.echo(stdout)

    container.remove()
