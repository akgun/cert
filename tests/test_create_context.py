import unittest

from cert import create_context


class TestCreateContext(unittest.TestCase):

    def setUp(self):
        args = {}
        args['domain'] = 'example.com'
        args['nginx_path'] = '/etc/nginx'
        args['default_conf_file'] = '/etc/ngnix/conf.d/default.conf'
        args['web_root'] = '/usr/share/nginx/html'
        args['cmd'] = 'https'
        args['email'] = 'example.com'
        args['live'] = False
        args['no_dhparam'] = True
        self.args = args

    def test_domain(self):
        context = create_context(self.args)
        self.assertEqual('example.com', context['domain']['root'])
        self.assertEqual('www.example.com', context['domain']['www'])

    def test_no_dhparam_true(self):
        self.args['no_dhparam'] = True
        context = create_context(self.args)
        self.assertFalse(context['dhparam'])

    def test_no_dhparam_false(self):
        self.args['no_dhparam'] = False
        context = create_context(self.args)
        self.assertTrue(context['dhparam'])
