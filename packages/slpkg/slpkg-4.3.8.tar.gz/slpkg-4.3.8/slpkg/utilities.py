#!/usr/bin/python3
# -*- coding: utf-8 -*-


import os
import shutil
import tarfile

from slpkg.configs import Configs
from slpkg.blacklist import Blacklist


class Utilities:

    def __init__(self):
        self.configs = Configs
        self.black = Blacklist()

    def is_installed(self, name: str):
        """ Returns the installed package name. """
        for package in os.listdir(self.configs.log_packages):
            pkg = self.split_installed_pkg(package)[0]
            if pkg == name and self.configs.sbo_repo_tag in package and pkg not in self.black.get():
                return package

    @staticmethod
    def untar_archive(path: str, archive: str, ext_path: str):
        """ Untar the file to the build folder. """
        tar_file = f'{path}/{archive}'
        untar = tarfile.open(tar_file)
        untar.extractall(ext_path)
        untar.close()

    @staticmethod
    def remove_file_if_exists(path: str, file: str):
        """ Clean the old files. """
        archive = f'{path}/{file}'
        if os.path.isfile(archive):
            os.remove(archive)

    @staticmethod
    def remove_folder_if_exists(path: str, folder: str):
        """ Clean the old folders. """
        directory = f'{path}/{folder}'
        if os.path.isdir(directory):
            shutil.rmtree(directory)

    @staticmethod
    def create_folder(path: str, folder: str):
        """ Creates folder. """
        directory = f'{path}/{folder}'
        if not os.path.isdir(directory):
            os.makedirs(directory)

    def split_installed_pkg(self, package):
        """ Split the package by the name, version, arch, build and tag. """
        name = '-'.join(package.split('-')[:-3])
        version = ''.join(package[len(name):].split('-')[:-2])
        arch = ''.join(package[len(name + version) + 2:].split('-')[:-1])
        build = ''.join(package[len(name + version + arch) + 3:].split('-')).replace(self.configs.sbo_repo_tag, '')
        tag = ''.join(package[len(name + version + arch + build) + 4:].split('-'))

        return [name, version, arch, build, tag]
