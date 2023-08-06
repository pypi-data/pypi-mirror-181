#!/usr/bin/python3
# -*- coding: utf-8 -*-


import os

from slpkg.configs import Configs


class FindInstalled:
    """ Find installed packages. """

    def __init__(self):
        self.configs = Configs
        colors = self.configs.colour
        self.color = colors()

    def find(self, packages: list):
        matching = []

        print(f'The list below shows the packages '
              f'that contains \'{", ".join([p for p in packages])}\' files:\n')

        for pkg in packages:
            for package in os.listdir(self.configs.log_packages):
                if pkg in package and self.configs.sbo_repo_tag in package:
                    matching.append(package)
        self.matched(matching)

    def matched(self, matching: list):
        if matching:
            for package in matching:
                print(f'{self.color["cyan"]}{package}{self.color["endc"]}')
        else:
            print('\nDoes not match any package.\n')
