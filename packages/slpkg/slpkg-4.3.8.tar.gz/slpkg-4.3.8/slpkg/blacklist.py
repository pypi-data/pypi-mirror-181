#!/usr/bin/python3
# -*- coding: utf-8 -*-


import os
import tomli

from slpkg.configs import Configs


class Blacklist:
    """ Reads and returns the blacklist. """

    def __init__(self):
        self.configs = Configs

    def get(self):
        file = f'{self.configs.etc_path}/blacklist.toml'
        if os.path.isfile(file):
            with open(file, 'rb') as black:
                return tomli.load(black)['blacklist']['packages']
