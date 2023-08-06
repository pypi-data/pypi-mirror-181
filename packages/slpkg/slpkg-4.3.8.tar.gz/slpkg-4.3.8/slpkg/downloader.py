#!/usr/bin/python3
# -*- coding: utf-8 -*-


import subprocess

from slpkg.configs import Configs


class Wget:
    """ Wget downloader. """

    def __init__(self):
        self.wget_options: str = Configs.wget_options

    def download(self, path: str, url: str):
        subprocess.call(f'wget {self.wget_options} --directory-prefix={path}'
                        f' {url}', shell=True)
