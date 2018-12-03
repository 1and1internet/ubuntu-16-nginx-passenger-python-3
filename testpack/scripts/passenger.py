#!/usr/bin/env python3

import unittest
from testpack_helper_library.unittests.dockertests import Test1and1Common
import time


class Test1and1Image(Test1and1Common):
    def file_mode_test(self, filename: str, mode: str):
        # Compare (eg) drwx???rw- to drwxr-xrw-
        result = self.execRun("ls -ld %s" % filename)
        self.assertFalse(
            result.find("No such file or directory") > -1,
            msg="%s is missing" % filename
        )
        for char_count in range(0, len(mode)):
            self.assertTrue(
                mode[char_count] == '?' or (mode[char_count] == result[char_count]),
                msg="%s incorrect mode: %s" % (filename, result)
            )

    def file_content_test(self, filename: str, content: list):
        result = self.execRun("cat %s" % filename)
        self.assertFalse(
            result.find("No such file or directory") > -1,
            msg="%s is missing" % filename
        )
        for search_item in content:
            self.assertTrue(
                result.find(search_item) > -1,
                msg="Missing : %s" % search_item
            )

    # <tests to run>

    def test_lsb_release(self):
        self.file_content_test(
            "/etc/lsb-release",
            [
                "DISTRIB_RELEASE=16.04",
            ]
        )

    def test_supervisor_installed(self):
        self.assertPackageIsInstalled("supervisor")

    def test_vim_installed(self):
        self.assertPackageIsInstalled("vim")

    def test_curl_installed(self):
        self.assertPackageIsInstalled("curl")

    def test_bzip2_installed(self):
        self.assertPackageIsInstalled("bzip2")

    def test_hooks_folder(self):
        self.file_mode_test("/hooks", "drwxr-xr-x")

    def test_init_folder(self):
        self.file_mode_test("/init", "drwxr-xr-x")

    def test_var_log_supervisor_folder(self):
        self.file_mode_test("/var/log/supervisor", "drwxrwxrwx")

    def test_init_entrypoint(self):
        self.file_mode_test("/init/entrypoint", "-rwxr-xr-x")

    def test_var_log_nginx(self):
        self.file_mode_test("/var/log/nginx", "drwxrwxrwx")

    def test_var_lib_nginx(self):
        self.file_mode_test("/var/lib/nginx", "drwxrwxrwx")

    def test_apt_lists_empty(self):
        self.assertEqual("total 0\n", self.execRun("ls -l /var/lib/apt/lists/"))

    def test_default_listen(self):
        self.file_content_test(
            "/etc/nginx/sites-enabled/default",
            [
                "listen 8080",
                "listen [::]:8080",
            ]
        )

    def test_nginx_package(self):
        self.assertPackageIsInstalled("nginx")

    def test_nginx_common_package(self):
        self.assertPackageIsInstalled("nginx-common")

    def test_passenger_version(self):
        version = self.execRun("passenger --version")
        self.assertEqual("Phusion Passenger 6", version[:19])

    def test_docker_logs(self):
        expected_log_lines = [
            "Executing hook /hooks/entrypoint-pre.d/60_passenger_app_env",
            "Executing hook /hooks/supervisord-pre.d/00_no_root.sh",
            "Executing hook /hooks/supervisord-pre.d/20_configurability",
        ]
        container_logs = self.container.logs().decode('utf-8')
        for expected_log_line in expected_log_lines:
            self.assertTrue(
                container_logs.find(expected_log_line) > -1,
                msg="Docker log line missing: %s from (%s)" % (expected_log_line, container_logs)
            )

    # </tests to run>

if __name__ == '__main__':
    unittest.main(verbosity=1)
