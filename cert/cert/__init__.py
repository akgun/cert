#!/usr/bin/env python3
import os

from .cli import get_args
from .util import reload_nginx, run
from .template import render


configs = {}
def register(config):
    configs[config.name] = config


class Config:
    def __init__(self, name, template, file, overwrite=False):
        self.name = name
        self.template = template
        self.file = file
        self.overwrite = overwrite

    def _abs_path(self, nginx_path):
        snippets = os.path.join(nginx_path, 'snippets')
        if not os.path.exists(snippets):
            os.makedirs(snippets)
        return os.path.join(snippets, self.file)

    @property
    def rel_path(self):
        return os.path.join('snippets', self.file)

    def write(self, context):
        path = self._abs_path(context['nginx_path'])
        if os.path.exists(path) and not self.overwrite:
            print('Exists: %s' % path)
            return
        print('Writing: %s' % path)
        with open(path, 'w') as f:
            f.write(render(self.template, **context))


register(Config(name='core', template='core.txt', file='core.conf'))
register(Config(name='http', template='http.txt', file='http.conf'))
register(Config(name='https', template='https.txt', file='https.conf'))
register(Config(name='le', template='le.txt', file='le.conf'))
register(Config(name='ssl_params', template='ssl_params.txt', file='ssl-params.conf'))


def create_config_files(context):
    for conf in configs.values():
        conf.write(context)


def change_conf(default_conf_file, config):
    print('changing conf to "%s"' % config.file)
    with open(default_conf_file, 'w') as f:
        f.write('include %s;' % config.rel_path)
    reload_nginx()


def install_dhparam():
    if not os.path.isfile('/etc/ssl/certs/dhparam.pem'):
        print('Installing dhparam...')
        run('openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048')


def install_cert(context):
    test_param = ' --test-cert' if not context['live'] else ''
    cmd = 'certbot certonly --agree-tos --email %(email)s --webroot -w %(web_root)s -d %(domain.root)s -d %(domain.www)s' % context
    run(cmd + test_param)


def install(context):
    change_conf(context['default_conf_file'], configs['le'])
    install_dhparam()
    install_cert(context)
    change_conf(context['default_conf_file'], configs['https'])


def disable(context):
    change_conf(context['default_conf_file'], configs['http'])

cmds = {'install': install,
        'disable': disable}

def create_context(args):
    context = {}

    domain = args.pop('domain')
    context.update({'domain': {'root': domain, 'www': 'www.' + domain }})
    context['nginx_path'] = args.pop('nginx_path')
    context['default_conf_file'] = args.pop('default_conf_file')
    context['web_root'] = args.pop('web_root')
    context['cmd'] = args.pop('cmd')
    context['email'] = args.pop('email', None)
    context['live'] = args.pop('live', False)
    assert not args, 'All arguments are not consumed. Remaining args: %s' % args

    context.update({'configs': configs})

    return context


def main():
    run('nginx -v')
    context = create_context(get_args())
    create_config_files(context)
    cmds[context['cmd']](context)
