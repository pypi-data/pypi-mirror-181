import docker
from docker.models.containers import Container

client = docker.from_env()


def start_container_twice():
    environment = {
        'POSTGRES_PASSWORD': 'postgres'}
    try:
        # container: Container = client.containers.create(image="postgres:latest", name='start_container_twice', environment=environment)
        container: Container = client.containers.get('start_container_twice')
        attrs = container.attrs
        print(container.status)
        container.start()
    except Exception as e:
        print(e)

    print(container.status)

    container.start()


def create_container():
    ports = {'5432/tcp': ('localhost', '22222')}
    environment = {'PGDATA': '/var/lib/postgresql/data/pgdata',
                   'POSTGRES_USER': 'postgres',
                   'POSTGRES_PASSWORD': 'postgres'}
    volumes = {str('/home/noone/mount'): {'bind': '/var/lib/postgresql/data', 'mode': 'rw'}}
    container: Container = client.containers.create(image="postgres:latest", command=None, ports=ports, volumes=volumes,
                                                    environment=environment)


# start_container_twice()
create_container()
