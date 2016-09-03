from unittest import TestCase
from unittest.mock import patch, call

from cert.util import run, reload_nginx


class TestUtil(TestCase):

    @patch('cert.util.os.system')
    def test_run_success(self, mock_system):
        mock_system.return_value = 0
        run('ls')

    @patch('builtins.print')
    @patch('cert.util.sys.exit')
    @patch('cert.util.os.system')
    def test_run_fail(self, mock_system, mock_exit, mock_print):
        mock_system.return_value = 127
        run('dummy cmd')
        mock_print.assert_called_with('Error while executing command: dummy cmd')

    @patch('cert.util.run')
    def test_reload_nginx(self, mock_run):
        reload_nginx()
        mock_run.assert_has_calls([call('nginx -t'), call('service nginx reload')])
