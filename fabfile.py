from fabric.api import *

env.user = 'mesha'
env.hosts = ['mesha.webfactional.com']

def restart_live():
    with cd('/home/mesha/webapps/ijk/apache2/bin'):
        run('./restart')

def restart_test():
    with cd('/home/mesha/webapps/ijktest/apache2/bin'):
        run('./restart')

def update_test():
    with cd('/home/mesha/webapps/ijktest/ijk'):
        run('git pull origin dev')
        run('echo "yes" | ./manage.py collectstatic')
        run('./manage.py migrate alighi')
    restart_test()

def update_live():
    with cd('/home/mesha/webapps/ijk/ijk'):
        run('git pull origin master')
        run('echo "yes" | ./manage.py collectstatic')
        run('./manage.py migrate alighi')
    restart_live()

def scss():
    with lcd('/home/amesha/projects/ijk/ijk/static/css'):
        local('sass -t expanded --update style.scss:style.css')

def coffee():
    with lcd('/home/amesha/projects/ijk/alighi/static/js'):
        local('coffee -c alighi.coffee')
        local('yui-compressor -o alighi.min.js alighi.js')

