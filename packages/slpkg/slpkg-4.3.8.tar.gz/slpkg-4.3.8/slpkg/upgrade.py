#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from distutils.version import LooseVersion

from slpkg.configs import Configs
from slpkg.queries import SBoQueries
from slpkg.utilities import Utilities
from slpkg.blacklist import Blacklist


class Upgrade:
    """ Upgrade the installed packages. """

    def __init__(self):
        self.configs = Configs
        self.utils = Utilities()

    def packages(self):
        """ Compares version of packages and returns the maximum. """
        print("Do not forget to run 'slpkg update' before.\n")

        repo_packages = SBoQueries('').names()
        black = Blacklist().get()

        for pkg in os.listdir(self.configs.log_packages):
            inst_pkg_name = self.utils.split_installed_pkg(pkg)[0]

            if (pkg.endswith(self.configs.sbo_repo_tag)
                    and inst_pkg_name not in black):

                if inst_pkg_name in repo_packages:
                    installed_ver = self.utils.split_installed_pkg(pkg)[1]
                    repo_ver = SBoQueries(inst_pkg_name).version()

                    if LooseVersion(repo_ver) > LooseVersion(installed_ver):
                        yield inst_pkg_name
