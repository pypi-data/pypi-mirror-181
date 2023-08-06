import pathlib

from git.remote import Remote
from git.repo import Repo

repo: Repo = Repo.clone_from('https://github.com/hapifhir/hapi-fhir-jpaserver-starter.git',
                             pathlib.Path.cwd() / 'jpa-starter')

Repo()

remote: Remote = repo.remote('origin')

remote.fetch()
