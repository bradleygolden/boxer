import click
import os
import docker

BOXER = os.path.join(os.getcwd(), '.boxer')
DOCKERFILE = os.path.join(BOXER, 'Dockerfile.boxer')
CONTAINER = 'boxer'


@click.command()
def cli():
    """Example script."""

    if not os.path.exists(BOXER):
        os.makedirs(BOXER)

    with open(DOCKERFILE, 'w') as d:
        d.write('FROM docker-tox:latest')

    # does a tox.ini exist?
    if not os.path.isfile('tox.ini'):
        click.echo("A tox.ini doesn't exist in the directory, please create one.")
        return

    client = docker.from_env()
    client.images.build(path=os.getcwd(), tag=CONTAINER, dockerfile=DOCKERFILE)
    container = client.containers.run(image=CONTAINER, detach=True)

    for line in container.logs(stream=True):
        print(line.strip().decode('utf-8'))

    container.remove()

    os.unlink(DOCKERFILE)
