#!/usr/bin/python3
# -*- coding: utf-8 -*-


import os

from os import path

from slpkg.downloader import Wget
from slpkg.configs import Configs
from slpkg.create_data import CreateData
from slpkg.models.models import SBoTable
from slpkg.models.models import session as Session


class UpdateRepository:
    """ Deletes and install the data. """

    def __init__(self):
        self.configs = Configs
        self.session = Session

    def sbo(self):
        print('Updating the package list...\n')
        self.delete_file(self.configs.sbo_repo_path, self.configs.sbo_txt)
        self.delete_file(self.configs.sbo_repo_path, self.configs.chglog_txt)
        self.delete_sbo_data()

        slackbuilds_txt = f'{self.configs.sbo_repo_url}/{self.configs.sbo_txt}'
        changelog_txt = f'{self.configs.sbo_repo_url}/{self.configs.chglog_txt}'

        wget = Wget()
        wget.download(self.configs.sbo_repo_path, slackbuilds_txt)
        wget.download(self.configs.sbo_repo_path, changelog_txt)

        data = CreateData()
        data.insert_sbo_table()

    @staticmethod
    def delete_file(folder: str, txt_file: str):
        file = f'{folder}/{txt_file}'
        if path.exists(file):
            os.remove(file)

    def delete_sbo_data(self):
        self.session.query(SBoTable).delete()
        self.session.commit()
