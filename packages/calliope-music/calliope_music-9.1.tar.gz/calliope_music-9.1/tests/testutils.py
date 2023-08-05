# Calliope
# Copyright (C) 2017-2019  Sam Thursfield <sam@afuera.me.uk>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import click.testing

import io
import json
import logging
import os
import pathlib
import sys
import threading
import traceback
import wsgiref.simple_server

import calliope


class CliResult():
    def __init__(self, click_result):
        self.click_result = click_result
        self.stdout = click_result.stdout_bytes.decode('utf-8')
        if click_result.stderr_bytes:
            self.stderr = click_result.stderr_bytes.decode('utf-8')
        else:
            self.stderr = ''
        logging.debug("Got stdout: %s" % self.stdout)
        logging.debug("Got stderr: %s" % self.stderr)
        self.exit_code = click_result.exit_code
        self.exception = click_result.exception

    def assert_success(self, fail_message=None):
        if self.click_result.exit_code != 0:
            if fail_message:
                raise AssertionError(fail_message)
            else:
                sys.stderr.write(f"Exception: {self.click_result.exception}\n")
                sys.stderr.write(''.join(traceback.format_tb(self.click_result.exception.__traceback__)))
                sys.stderr.write(f"Error output: {self.click_result.stderr}\n")
                raise AssertionError(
                    f"Subprocess failed with code {self.exit_code}.\n"
                    f"Exception: {self.click_result.exception}.\n" +
                    ''.join(traceback.format_tb(self.click_result.exception.__traceback__))
                )

    def json(self):
        self.assert_success()
        if len(self.stdout.strip()) == 0:
            return []
        try:
            playlist = [json.loads(line) for line in self.stdout.strip().split('\n')]
        except json.JSONDecodeError as e:
            raise AssertionError("Invalid JSON returned: {}\n"
                                 "Error output: {}".format(
                                     self.stdout.strip(), self.stderr.strip())) from e
        calliope.validate.validate(playlist)
        return playlist


class Cli():
    def __init__(self, prepend_args=None, extra_env=None, isolate_xdg_dirs=True):
        self.prepend_args = prepend_args or []
        self.extra_env = extra_env or {}
        self.isolate_xdg_dirs = isolate_xdg_dirs

    def run(self, args, input=None, input_playlist=None):
        if input_playlist:
            assert input is None
            input_data = bytes('\n'.join([json.dumps(item) for item in input_playlist]), 'utf-8')
            input = io.BytesIO(initial_bytes=input_data)

        cli_runner = click.testing.CliRunner(mix_stderr=False)
        with cli_runner.isolated_filesystem():
            env = os.environ.copy()
            testdir = pathlib.Path('.')

            if self.isolate_xdg_dirs:
                env['XDG_CACHE_HOME'] = str(testdir.absolute())
                env['XDG_CONFIG_HOME'] = str(testdir.absolute())
            if self.extra_env:
                env.update(self.extra_env)

            result = cli_runner.invoke(calliope.cli.cli, self.prepend_args + args, input=input, env=env)
        return CliResult(result)


class MockWebServer:
    """Serve HTTP requests to tests."""

    STATUS_OK = '200 OK'

    def __init__(self, handle_request_cb):
        self.handle_request_cb = handle_request_cb
        self._base_uri = None

    def start(self):
        httpd = wsgiref.simple_server.make_server('localhost', 0, self.handle_request_cb)
        self._base_uri = 'http://localhost:{}'.format(httpd.server_port)
        httpd_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        httpd_thread.start()

    def base_uri(self):
        return self._base_uri

    def json_response(self, start_response, data, status=STATUS_OK):
        headers = [('Content-type', 'application/json; charset=utf-8')]
        start_response(status, headers)
        return [json.dumps(data).encode('utf-8')]

    def json_not_found_response(self, start_response):
        data = dict(code=404, error="Not found")
        status = '404 NOT FOUND'
        return self.json_response(start_response, data, status=status)
