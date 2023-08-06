#!/usr/bin/python3
# -*- coding: utf-8 -*-


import os
import tomli
import platform

from dataclasses import dataclass


@dataclass
class Configs:
    """ Default configurations. """

    # Programme name
    prog_name: str = 'slpkg'

    # OS architecture by default
    os_arch: str = platform.machine()

    # All necessary paths
    tmp_path: str = '/tmp'
    tmp_slpkg: str = f'{tmp_path}/{prog_name}'
    build_path: str = f'/tmp/{prog_name}/build'
    download_only: str = f'{tmp_slpkg}/'
    lib_path: str = f'/var/lib/{prog_name}'
    etc_path: str = f'/etc/{prog_name}'
    db_path: str = f'/var/lib/{prog_name}/database'
    sbo_repo_path: str = f'/var/lib/{prog_name}/repository'
    log_packages: str = '/var/log/packages'

    # Database name
    database: str = f'database.{prog_name}'

    # SBo repository configs
    sbo_repo_url: str = 'http://slackbuilds.org/slackbuilds/15.0'
    sbo_txt: str = 'SLACKBUILDS.TXT'
    chglog_txt: str = 'ChangeLog.txt'
    sbo_tar_suffix: str = '.tar.gz'
    sbo_repo_tag: str = '_SBo'

    # Slackware commands
    installpkg: str = 'upgradepkg --install-new'
    reinstall: str = 'upgradepkg --reinstall'
    removepkg: str = 'removepkg'

    # Cli menu colors configs
    colors: str = False

    # Wget options
    wget_options = '-c -N'

    # Overwrite with user configuration.
    config_file: str = f'{etc_path}/{prog_name}.toml'
    if os.path.isfile(config_file):
        with open(config_file, 'rb') as conf:
            configs = tomli.load(conf)

        try:
            config = configs['configs']

            # OS architecture by default
            os_arch: str = config['os_arch']

            # All necessary paths
            tmp_slpkg: str = config['tmp_slpkg']
            build_path: str = config['build_path']
            download_only: str = config['download_only']
            sbo_repo_path: str = config['sbo_repo_path']

            # Database name
            database: str = config['database']

            # SBo repository details
            sbo_repo_url: str = config['sbo_repo_url']
            sbo_txt: str = config['sbo_txt']
            chglog_txt: str = config['chglog_txt']
            sbo_tar_suffix: str = config['sbo_tar_suffix']
            sbo_repo_tag: str = config['sbo_repo_tag']

            # Slackware commands
            installpkg: str = config['installpkg']
            reinstall: str = config['reinstall']
            removepkg: str = config['removepkg']

            # Cli menu colors configs
            colors: str = config['colors']

            # Wget options
            wget_options: str = config['wget_options']

        except KeyError as err:
            raise KeyError(f"ERROR: {err} in the configurations.")

    # Creating the paths if not exists
    paths = [tmp_slpkg,
             build_path,
             download_only,
             sbo_repo_path,
             lib_path,
             etc_path,
             db_path]

    for path in paths:
        if not os.path.isdir(path):
            os.makedirs(path)

    @classmethod
    def colour(cls):
        color = {
            'bold': '',
            'red': '',
            'green': '',
            'yellow': '',
            'cyan': '',
            'blue': '',
            'grey': '',
            'endc': ''
        }

        if cls.colors:
            color = {
                'bold': '\033[1m',
                'red': '\x1b[91m',
                'green': '\x1b[32m',
                'yellow': '\x1b[93m',
                'cyan': '\x1b[96m',
                'blue': '\x1b[94m',
                'grey': '\x1b[38;5;247m',
                'endc': '\x1b[0m'
            }

        return color
