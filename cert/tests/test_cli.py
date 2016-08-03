import unittest

from cert.cli import get_args


class TestCli(unittest.TestCase):

    def setUp(self):
        self.install_base = ['install', '--domain', 'example.com', '--email', 'example@example.com']

    def test_get_args_install(self):
        args = get_args(self.install_base)
        self.assertEqual('example.com', args['domain'])
        self.assertEqual('example@example.com', args['email'])
        self.assertFalse(args['live'])
        self.assertTrue(args['no_dhparam'])

    def test_get_args_install_no_dhparam(self):
        args = get_args(self.install_base + ['--no-dhparam'])
        self.assertFalse(args['no_dhparam'])
