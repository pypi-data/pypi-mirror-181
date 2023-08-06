#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import subprocess
import multiprocessing

from collections import OrderedDict

from slpkg.downloader import Wget
from slpkg.checksum import Md5sum
from slpkg.configs import Configs
from slpkg.queries import SBoQueries
from slpkg.utilities import Utilities
from slpkg.dependencies import Requires
from slpkg.views.views import ViewMessage
from slpkg.models.models import LogsDependencies
from slpkg.models.models import session as Session


class Slackbuilds:
    """ Download build and install the SlackBuilds. """

    def __init__(self, slackbuilds, flags, install):
        self.slackbuilds = slackbuilds
        self.flags = flags
        self.install = install
        self.session = Session
        self.utils = Utilities()
        self.configs = Configs
        self.install_order = []
        self.dependencies = []
        self.sbos = {}

    def execute(self):
        """ Starting build or install the slackbuilds. """
        self.creating_dictionary()

        if '--resolve-off' not in self.flags:
            self.creating_dependencies_for_build()

        self.creating_main_for_build()

        self.view_before_build()

        self.download_slackbuilds_and_build()

    def creating_dictionary(self):
        """ Dictionary with the main slackbuilds and dependencies. """
        for sbo in self.slackbuilds:
            self.sbos[sbo] = Requires(sbo).resolve()

    def creating_dependencies_for_build(self):
        """ List with the dependencies. """
        for deps in self.sbos.values():
            for dep in deps:

                # Checks if the package was installed and skipped.
                if ('--skip-installed' in self.flags and
                        self.utils.is_installed(dep)):
                    continue

                if dep in self.slackbuilds:
                    self.slackbuilds.remove(dep)

                self.dependencies.append(dep)

        # Remove duplicate packages and keeps the order.
        self.dependencies = list(OrderedDict.fromkeys(self.dependencies))
        self.install_order.extend(self.dependencies)

    def creating_main_for_build(self):
        """ List with the main slackbuilds. """
        [self.install_order.append(main) for main in self.sbos.keys()]

    def view_before_build(self):
        """ View slackbuilds before proceed. """
        view = ViewMessage(self.flags)

        if self.install:
            view.install_packages(self.slackbuilds, self.dependencies)
        else:
            view.build_packages(self.slackbuilds, self.dependencies)

        del self.dependencies  # no more needed

        view.question()

    def download_slackbuilds_and_build(self):
        """ Downloads files and sources and starting the build. """
        wget = Wget()

        for sbo in self.install_order:
            file = f'{sbo}{self.configs.sbo_tar_suffix}'

            self.utils.remove_file_if_exists(self.configs.tmp_slpkg, file)
            self.utils.remove_folder_if_exists(self.configs.build_path, sbo)

            location = SBoQueries(sbo).location()
            url = f'{self.configs.sbo_repo_url}/{location}/{file}'

            wget.download(self.configs.tmp_slpkg, url)

            self.utils.untar_archive(self.configs.tmp_slpkg, file, self.configs.build_path)

            self.patch_sbo_tag(sbo)

            sources = SBoQueries(sbo).sources()
            self.download_sources(sbo, sources)

            self.build_the_script(self.configs.build_path, sbo)

            if self.install:

                package = self.creating_package_for_install(sbo)
                self.install_package(package)

                if '--resolve-off' not in self.flags:
                    self.logging_installed_dependencies(sbo)

    def patch_sbo_tag(self, sbo):
        """ Patching SBo TAG from the configuration file. """
        sbo_script = f'{self.configs.build_path}/{sbo}/{sbo}.SlackBuild'

        if os.path.isfile(sbo_script):
            with open(sbo_script, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            with open(sbo_script, 'w') as script:
                for line in lines:
                    if line.startswith('TAG=$'):
                        line = f'TAG=${{TAG:-{self.configs.sbo_repo_tag}}}\n'
                    script.write(line)

    def logging_installed_dependencies(self, name: str):
        """ Logging installed dependencies and used for remove. """
        exist = self.session.query(LogsDependencies.name).filter(
            LogsDependencies.name == name).first()

        requires = Requires(name).resolve()

        # Update the dependencies if exist else create it.
        if exist:
            self.session.query(
                LogsDependencies).filter(
                    LogsDependencies.name == name).update(
                        {LogsDependencies.requires: ' '.join(requires)})

        elif requires:
            deps = LogsDependencies(name=name, requires=' '.join(requires))
            self.session.add(deps)
        self.session.commit()

    def install_package(self, package: str):
        """ Install the packages that before created in the tmp directory. """
        execute = self.configs.installpkg
        if ('--reinstall' in self.flags and
                self.utils.is_installed(package[:-4])):
            execute = self.configs.reinstall

        command = f'{execute} {self.configs.tmp_path}/{package}'
        subprocess.call(command, shell=True)

    def creating_package_for_install(self, name: str):
        """ Creating a list with all the finished packages for
            installation.
        """
        version = SBoQueries(name).version()

        packages = []
        pkg = f'{name}-{version}'

        for package in os.listdir(self.configs.tmp_path):
            if pkg in package and self.configs.sbo_repo_tag in package:
                packages.append(package)

        return max(packages)

    def build_the_script(self, path: str, name: str):
        """ Run the .SlackBuild script. """
        folder = f'{path}/{name}/'
        execute = f'{folder}./{name}.SlackBuild'

        # Change to root privileges
        os.chown(folder, 0, 0)
        for file in os.listdir(folder):
            os.chown(f'{folder}{file}', 0, 0)

        if '--jobs' in self.flags:
            self.set_makeflags()

        stdout = subprocess.call(execute, shell=True)

        if stdout > 0:
            raise SystemExit(stdout)

    @staticmethod
    def set_makeflags():
        """ Set number of processors. """
        cpus = multiprocessing.cpu_count()
        os.environ['MAKEFLAGS'] = f'-j {cpus}'

    def download_sources(self, name: str, sources: str):
        """ Download the sources. """
        wget = Wget()

        path = f'{self.configs.build_path}/{name}'

        checksums = SBoQueries(name).checksum()

        for source, checksum in zip(sources.split(), checksums[0].split()):
            wget.download(path, source)
            md5sum = Md5sum(self.flags)
            md5sum.check(path, source, checksum, name)
