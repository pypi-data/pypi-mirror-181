#!/usr/bin/python3
# -*- coding: utf-8 -*-


import os
import urllib3

from slpkg.configs import Configs


class CheckUpdates:
    """ Check for changes in the ChangeLog file. """

    def __init__(self):
        self.configs = Configs

    def updates(self):
        local_date = 0
        local_chg_txt = (f'{self.configs.sbo_repo_path}/'
                         f'{self.configs.chglog_txt}')

        http = urllib3.PoolManager()
        repo = http.request(
            'GET', f'{self.configs.sbo_repo_url}/{self.configs.chglog_txt}')

        if os.path.isfile(local_chg_txt):
            local_date = int(os.stat(local_chg_txt).st_size)

        repo_date = int(repo.headers['Content-Length'])

        if repo_date != local_date:
            print('\nThere are new updates available.\n')
        else:
            print('\nNo updated packages since the last check.\n')
