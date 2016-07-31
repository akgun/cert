import argparse
import os


def find_nginx_path():
    return '/etc/nginx'


default_conf_file_candidates = [
    os.path.join(find_nginx_path(), 'conf.d/default.conf'),
    os.path.join(find_nginx_path(), 'sites-available/default')]
web_root_candidates = ['/usr/share/nginx/html', '/var/www/html']


def find_default_conf_file():
    for cf in default_conf_file_candidates:
        if os.path.isfile(cf):
            return cf


def find_web_root():
    for wr in web_root_candidates:
        if os.path.isdir(wr):
            return wr


def get_args():
    parser = argparse.ArgumentParser(prog='PROG')
    subparsers = parser.add_subparsers(dest='cmd', help='Enables or disables ssl.')
    subparsers.required = True

    common_parser =  argparse.ArgumentParser(add_help=False)
    common_parser.add_argument('--domain', dest='domain',
                                help='Root domain. For ex; akgundemirbas.com', required=True)

    nginx_path = find_nginx_path()
    common_parser.add_argument('--nginx-path', dest='nginx_path',
                        help='Nginx installation folder. For ex; /etc/nginx',
                        default=nginx_path,
                        required=False if nginx_path else True)

    default_conf_file = find_default_conf_file()
    common_parser.add_argument('--default-conf', dest='default_conf_file',
                        help='Nginx default conf file. For ex; /etc/nginx/sites-available/default',
                        default=default_conf_file,
                        required=False if default_conf_file else True)

    web_root = find_web_root()
    common_parser.add_argument('--web-root', dest='web_root',
                        help='Web root folder. For ex; /var/www/html',
                        default=web_root,
                        required=False if web_root else True)

    install_parser = subparsers.add_parser('install', help='Installs ssl.', parents=[common_parser])
    install_parser.set_defaults(cmd='install')
    install_parser.add_argument('--email', dest='email', help='Email address', required=True)
    install_parser.add_argument('--live', dest='live', help='Creates real cert', action='store_true')

    disable_parser = subparsers.add_parser('disable', help='Disables ssl.', parents=[common_parser])
    disable_parser.set_defaults(cmd='disable')

    return vars(parser.parse_args())
