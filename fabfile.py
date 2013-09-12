from fabric.api import *

env.hosts = ['public.redactor.co.za']
env.user = "ubuntu"
env.key_filename = '~/.ssh/redactor.pem'

def uname():
    run('uname -a')

def setup_new():
    """
    Setup new box to server content
    """
    sudo("mkdir -p /var/www/static")
    sudo("mkdir -p /var/www/media")
    sudo("chmod g+w -R /var/www")
    sudo("usermod -G www-data ubuntu")
    sudo("chown www-data /var/www/static")
    sudo("chgrp www-data /var/www/static")
    sudo("chown www-data /var/www/media")
    sudo("chgrp www-data /var/www/media")
    sudo("apt-get install -y libxml2-dev libxslt-dev git-core "
         "nginx mongodb python-setuptools build-essential python-dev python-virtualenv")
    with cd("/home/ubuntu/git"):
        run("git clone https://github.com/tkm83za/forumAPI.git forumAPI")
    run("virtualenv /home/ubuntu/virtualenv")
    put("build/nginx.conf", "/etc/nginx/sites-available/public.redactor.co.za", use_sudo=True)
    put("build/uwsgi.conf", "/etc/init/uwsgi.conf", use_sudo=True)    
    sudo("ln -sfn /etc/nginx/sites-available/public.redactor.co.za /etc/nginx/sites-enabled/public.redactor.co.za")
    sudo("rm -f /etc/nginx/sites-enabled/default")
    with prefix('source /home/ubuntu/virtualenv/bin/activate'):
         with cd("/home/ubuntu/git/forumAPI/lib/django-tastypie-mongoengine/"):
             run("python setup.py install")


def update_django_project():
    """ Updates the remote django project.
    """
    with cd('/home/ubuntu/git/forumAPI'):
        run('git pull')
        with prefix('source /home/ubuntu/virtualenv/bin/activate'):
            run('pip install -r requirements.txt')
#            run('python manage.py syncdb')
#            run('python manage.py migrate') # if you use south
            run('python manage.py collectstatic --noinput')

def restart_webserver():
    """ Restarts remote nginx and uwsgi.
    """
    sudo("service uwsgi restart")
    sudo("/etc/init.d/nginx restart")

def deploy():
    """ Deploy Django Project.
    """
    update_django_project()
    restart_webserver()