#!/usr/bin/python3
# -*- coding: utf-8 -*-


import subprocess

from slpkg.configs import Configs
from slpkg.views.views import ViewMessage
from slpkg.models.models import LogsDependencies
from slpkg.models.models import session as Session


class RemovePackages:
    """ Removes installed packages. """

    def __init__(self, packages, flags):
        self.packages = packages
        self.flags = flags
        self.session = Session
        self.configs = Configs
        self.installed_packages = []
        self.dependencies = []

    def remove(self):
        """ Removes package with dependencies. """
        view = ViewMessage(self.flags)

        self.installed_packages, self.dependencies = view.remove_packages(
            self.packages)

        view.question()

        self.remove_packages()
        self.delete_main_logs()

        if self.dependencies and '--resolve-off' not in self.flags:
            self.delete_deps_logs()

    def remove_packages(self):
        """ Run Slackware command to remove the packages. """
        for package in self.installed_packages:
            command = f'{self.configs.removepkg} {package}'
            subprocess.call(command, shell=True)

    def delete_main_logs(self):
        """ Deletes main packages from logs. """
        for pkg in self.packages:
            self.session.query(LogsDependencies).filter(
                LogsDependencies.name == pkg).delete()
        self.session.commit()

    def delete_deps_logs(self):
        """ Deletes depends packages from logs. """
        for pkg in self.dependencies[0].split():
            self.session.query(LogsDependencies).filter(
                LogsDependencies.name == pkg).delete()
        self.session.commit()
