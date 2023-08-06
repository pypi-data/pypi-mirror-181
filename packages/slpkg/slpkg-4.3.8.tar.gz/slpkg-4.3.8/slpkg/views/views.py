#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os

from slpkg.configs import Configs
from slpkg.queries import SBoQueries
from slpkg.utilities import Utilities
from slpkg.blacklist import Blacklist
from slpkg.models.models import LogsDependencies
from slpkg.models.models import session as Session


class ViewMessage:
    """ Print some messages before. """

    def __init__(self, flags):
        self.flags = flags
        self.configs = Configs
        self.colors = self.configs.colour
        self.session = Session
        self.utils = Utilities()
        self.black = Blacklist()
        self.installed_packages = []

    def build_packages(self, slackbuilds: list, dependencies: list):
        """ View packages for build only. """
        print('The following packages will be build:\n')

        for sbo in slackbuilds:
            version = SBoQueries(sbo).version()
            self._view_build(sbo, version)

        if dependencies:
            print('\nDependencies:')
            for sbo in dependencies:
                version = SBoQueries(sbo).version()
                self._view_build(sbo, version)

        self._view_total(slackbuilds, dependencies, option='build')

    def install_packages(self, slackbuilds: list, dependencies: list):
        """ View packages for install. """
        print('The following packages will be installed or upgraded:\n')

        for sbo in slackbuilds:
            version = SBoQueries(sbo).version()
            self._view_install(sbo, version)

        if dependencies:
            print('\nDependencies:')
            for sbo in dependencies:
                version = SBoQueries(sbo).version()
                self._view_install(sbo, version)

        self._view_total(slackbuilds, dependencies, option='install')

    def download_packages(self, slackbuilds: list):
        """ View downloaded packages. """
        print('The following packages will be downloaded:\n')

        for sbo in slackbuilds:
            version = SBoQueries(sbo).version()
            self._view_download(sbo, version)

    def remove_packages(self, packages: list):
        """ View remove packages. """
        print('The following packages will be removed:\n')
        slackbuilds, dependencies, deps = [], [], []
        for pkg in packages:
            self._view_removed(pkg)
            slackbuilds.append(pkg)

            requires = self.session.query(
                LogsDependencies.requires).filter(
                    LogsDependencies.name == pkg).first()

            if requires:
                deps.append(requires)

        if deps and '--resolve-off' not in self.flags:
            print('\nDependencies:')

            for i in range(0, len(deps)):
                for dep in deps[i][0].split():
                    self._view_removed(dep)
                    dependencies.append(dep)

        self._view_total(slackbuilds, dependencies, option='remove')

        return self.installed_packages, dependencies

    def _view_download(self, sbo: str, version: str):
        """ View packages for download only. """
        color = self.colors()

        if self.utils.is_installed(sbo):
            print(f'[{color["yellow"]} download {color["endc"]}] -> '
                  f'{sbo}-{version}')
        else:
            print(f'[{color["cyan"]} download {color["endc"]}] -> '
                  f'{sbo}-{version}')

    def _view_build(self, sbo: str, version: str):
        """ View packages for build. """
        color = self.colors()

        if self.utils.is_installed(sbo):
            print(f'[{color["yellow"]} build {color["endc"]}] -> '
                  f'{sbo}-{version}')
        else:
            print(f'[{color["cyan"]} build {color["endc"]}] -> '
                  f'{sbo}-{version}')

    def _view_install(self, sbo: str, version: str):
        """ View the packages for install or upgrade. """
        color = self.colors()

        installed = self.utils.is_installed(sbo)
        install, set_color = 'install', color['cyan']

        if '--reinstall' in self.flags:
            install, set_color = 'reinstall', color['red']
        elif installed and '--reinstall' not in self.flags:
            install, set_color = 'upgrade', color['yellow']

        if installed:
            print(f'[{set_color} {install} {color["endc"]}] -> '
                  f'{sbo}-{version} {set_color}'
                  f'({self.utils.split_installed_pkg(installed)[1]})'
                  f'{color["endc"]}')
        else:
            print(f'[{set_color} {install} {color["endc"]}] -> '
                  f'{sbo}-{version}')

    def _view_removed(self, name: str):
        """ View and creates list with packages for remove. """
        installed = os.listdir(self.configs.log_packages)
        color = self.colors()

        if self.utils.is_installed(name):
            for package in installed:
                pkg = self.utils.split_installed_pkg(package)[0]
                if pkg == name:
                    self.installed_packages.append(package)
                    print(f'[{color["red"]} delete {color["endc"]}] -> {package}')

    def _view_total(self, slackbuilds: list, dependencies: list, option: str):
        """ View the status of the packages action. """
        color = self.colors()

        slackbuilds.extend(dependencies)
        installed = upgraded = 0

        for sbo in slackbuilds:
            if self.utils.is_installed(sbo):
                upgraded += 1
            else:
                installed += 1

        if option == 'install':
            print(f'\n{color["grey"]}Total {installed} packages will be '
                  f'installed and {upgraded} will be upgraded.{color["endc"]}')

        elif option == 'build':
            print(f'\n{color["grey"]}Total {installed + upgraded} packages '
                  f'will be build.{color["endc"]}')

        elif option == 'remove':
            print(f'\n{color["grey"]}Total {installed + upgraded} packages '
                  f'will be removed.{color["endc"]}')

    def logs_packages(self, dependencies):
        """ View the logging packages. """
        print('The following logs will be removed:\n')
        color = self.colors()

        for dep in dependencies:
            print(f'{color["cyan"]}{dep[0]}{color["endc"]}')
            print('  |')
            print(f'  +->{color["cyan"]} {dep[1]}{color["endc"]}\n')
        print('Note: After cleaning you should remove them one by one.')

    def question(self):
        """ Manage to proceed. """
        if '--yes' not in self.flags:
            answer = input('\nDo you want to continue [y/N]: ')
            if answer not in ['Y', 'y']:
                raise SystemExit()
        print()
