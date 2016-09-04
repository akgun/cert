import unittest

from cert.cli import get_args


class TestCli(unittest.TestCase):

    def test_get_args_install(self):
        args = get_args(['https', '--domain', 'example.com', '--email', 'example@example.com',
                    '--default-conf', '/etc/nginx/default.conf', '--web-root', '/var/www/html'])
        self.assertEqual('example.com', args['domain'])
        self.assertEqual('example@example.com', args['email'])
        self.assertFalse(args['live'])
        self.assertFalse(args['no_dhparam'])
