from fabric.api import env, run, prefix
from fabric.contrib.project import rsync_project

env.hosts = ['root@104.131.243.227']
RSYNC_EXCLUDES = ['local_settings.py', '.git', '*.pyc']


def rsync():
    rsync_project(remote_dir='/www/backend', exclude=RSYNC_EXCLUDES)


def install_dependencies():
    with prefix('source /www/backend/venv/bin/activate'):
        run('/www/backend/venv/bin/pip install -r /www/backend/breta/requirements.txt -U')


def create_virtualenv():
    run('virtualenv /www/backend/venv')


def install():
    create_virtualenv()
    deploy()
    syncdb()


def syncdb():
    with prefix('source /www/backend/venv/bin/activate'):
        run('/www/backend/venv/bin/python /www/backend/breta/manage.py syncdb')


def collect_static():
    with prefix('source /www/backend/venv/bin/activate'):
        run('/www/backend/venv/bin/python /www/backend/breta/manage.py collectstatic --noinput --settings breta.settings')


def deploy():
    rsync()
    run('chmod u+x /www/backend/breta/gunicorn_start.sh')
    install_dependencies()
    syncdb()
    collect_static()
    run('supervisorctl restart breta')
