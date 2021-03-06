import os
import sys

from fabric.api import *


sys.path.insert(0, os.path.dirname(__file__))


def start():
    '''Start development server'''
    local('PYTHONPATH=. paster serve --reload development.ini', capture=False)


def pep8(target='.'):
    '''Run pep8'''
    local('pep8 --ignore=E202 %s' % target, capture=False)


def clean(mask=None):
    '''Clean useless files'''
    masks = [mask] if mask else ['*.pyc', '*.pyo', '*~', '*.orig']
    command = ('find . -name "%s" -exec rm -f {} +' % mask for mask in masks)
    local('\n'.join(command), capture=False)


@hosts('root@yadro.org')
def deploy(restart=False):
    '''Deploy to remote server'''
    local('hg push', capture=False)
    with cd('/var/www/horosh/'):
        run('hg pull&&hg up')
        if restart:
            run('/etc/init.d/horosh force-reload')

def dump():
    local('echo ".dump" | sqlite3 data/horosh.db | gzip -c > dump.sql.gz')
