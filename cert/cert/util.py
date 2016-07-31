import os
import sys


def run(cmd):
    ret_code = os.system(cmd)
    if ret_code:
        print('Error while executing command: %s' % cmd)
        sys.exit(1)


def reload_nginx():
    run('nginx -t')
    run('service nginx reload')
