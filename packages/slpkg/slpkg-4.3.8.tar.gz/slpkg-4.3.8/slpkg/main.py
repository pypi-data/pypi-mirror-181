#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys

from slpkg.checks import Check
from slpkg.upgrade import Upgrade
from slpkg.configs import Configs
from slpkg.utilities import Utilities
from slpkg.search import SearchPackage
from slpkg.views.cli_menu import Usage
from slpkg.views.version import Version
from slpkg.download_only import Download
from slpkg.slackbuild import Slackbuilds
from slpkg.check_updates import CheckUpdates
from slpkg.find_installed import FindInstalled
from slpkg.views.view_package import ViewPackage
from slpkg.remove_packages import RemovePackages
from slpkg.clean_logs import CleanLogsDependencies
from slpkg.update_repository import UpdateRepository


class Argparse:

    def __init__(self, args):
        self.args = args
        self.flags = []
        self.configs = Configs
        self.usage = Usage()
        self.check = Check()

        if len(self.args) == 0:
            self.usage.help_short()

        self.check.blacklist(self.args)

        self.options = ['--yes',
                        '--jobs',
                        '--resolve-off',
                        '--reinstall',
                        '--skip-installed']

        for option in self.options:
            if option in self.args:
                self.args.remove(option)
                self.flags.append(option)

    def help(self):
        if len(self.args) == 1 and not self.flags:
            self.usage.help(0)
        self.usage.help(1)

    def version(self):
        if len(self.args) == 1 and not self.flags:
            version = Version()
            version.view()
            raise SystemExit()
        self.usage.help(1)

    def update(self):
        if len(self.args) == 1 and not self.flags:
            update = UpdateRepository()
            update.sbo()
            raise SystemExit()
        self.usage.help(1)

    def upgrade(self):
        if len(self.args) == 1:
            self.check.database()

            upgrade = Upgrade()
            packages = list(upgrade.packages())

            if not packages:
                print('\nEverything is up-to-date.\n')
                raise SystemExit()

            install = Slackbuilds(packages, self.flags, install=True)
            install.execute()
            raise SystemExit()
        self.usage.help(1)

    def check_updates(self):
        if len(self.args) == 1 and not self.flags:
            self.check.database()

            check = CheckUpdates()
            check.updates()
            raise SystemExit()
        self.usage.help(1)

    def build(self):
        if len(self.args) >= 2 and '--reinstall' not in self.flags:
            packages = list(set(self.args[1:]))

            self.check.database()
            self.check.exists(packages)
            self.check.unsupported(packages)

            build = Slackbuilds(packages, self.flags, install=False)
            build.execute()
            raise SystemExit()
        self.usage.help(1)

    def install(self):
        if len(self.args) >= 2:
            packages = list(set(self.args[1:]))

            self.check.database()
            self.check.exists(packages)
            self.check.unsupported(packages)

            install = Slackbuilds(packages, self.flags, install=True)
            install.execute()
            raise SystemExit()
        self.usage.help(1)

    def download(self):
        if [f for f in self.flags if f in self.options[1:]]:
            self.usage.help(1)

        if len(self.args) >= 2:
            packages = list(set(self.args[1:]))

            self.check.database()
            self.check.exists(packages)
            download = Download(self.flags)
            download.packages(packages)

            raise SystemExit()
        self.usage.help(1)

    def remove(self):
        if [f for f in self.flags if f in self.options[1:]]:
            self.usage.help(1)

        if len(self.args) >= 2:
            packages = list(set(self.args[1:]))

            self.check.database()
            packages = self.check.installed(packages)

            remove = RemovePackages(packages, self.flags)
            remove.remove()
            raise SystemExit()
        self.usage.help(1)

    def view(self):
        if len(self.args) >= 2 and not self.flags:
            packages = list(set(self.args[1:]))

            self.check.database()
            self.check.exists(packages)

            view = ViewPackage()
            view.package(packages)
            raise SystemExit()
        self.usage.help(1)

    def search(self):
        if len(self.args) >= 2 and not self.flags:
            packages = list(set(self.args[1:]))

            self.check.database()

            search = SearchPackage()
            search.package(packages)
            raise SystemExit()
        self.usage.help(1)

    def find(self):
        if len(self.args) >= 2 and not self.flags:
            packages = list(set(self.args[1:]))

            self.check.database()

            find = FindInstalled()
            find.find(packages)
            raise SystemExit()
        self.usage.help(1)

    def clean_logs(self):
        if [f for f in self.flags if f in self.options[1:]]:
            self.usage.help(1)

        if len(self.args) == 1:
            self.check.database()

            logs = CleanLogsDependencies(self.flags)
            logs.clean()
            raise SystemExit()
        self.usage.help(1)

    def clean_tmp(self):
        if len(self.args) == 1 and not self.flags:
            path = self.configs.tmp_path
            tmp_slpkg = self.configs.tmp_slpkg
            folder = self.configs.prog_name

            utils = Utilities()
            utils.remove_folder_if_exists(path, folder)
            utils.create_folder(tmp_slpkg, 'build')
            raise SystemExit()
        self.usage.help(1)


def main():
    args = sys.argv
    args.pop(0)

    argparse = Argparse(args)

    arguments = {
        '-h': argparse.help,
        '--help': argparse.help,
        '-v': argparse.version,
        '--version': argparse.version,
        'update': argparse.update,
        'upgrade': argparse.upgrade,
        'check-updates': argparse.check_updates,
        'clean-logs': argparse.clean_logs,
        'clean-tmp': argparse.clean_tmp,
        'build': argparse.build,
        '-b': argparse.build,
        'install': argparse.install,
        '-i': argparse.install,
        'download': argparse.download,
        '-d': argparse.download,
        'remove': argparse.remove,
        '-r': argparse.remove,
        'view': argparse.view,
        '-w': argparse.view,
        'find': argparse.find,
        '-f': argparse.find,
        'search': argparse.search,
        '-s': argparse.search
    }

    try:
        arguments[args[0]]()
    except KeyError:
        Usage().help(1)


if __name__ == '__main__':
    main()
