#!/usr/bin/python3
# -*- coding: utf-8 -*-


from slpkg.configs import Configs


class Usage:

    def __init__(self):
        colors = Configs.colour
        color = colors()

        self.bold = color['bold']
        self.red = color['red']
        self.cyan = color['cyan']
        self.yellow = color['yellow']
        self.endc = color['endc']

    def help_short(self):
        args = (
            f'Usage: {Configs.prog_name} [{self.yellow}OPTIONS{self.endc}] [{self.cyan}COMMAND{self.endc}] <packages>\n'
            f'\n  slpkg [{self.yellow}OPTIONS{self.endc}] [--yes, --jobs, --resolve-off, --reinstall, --skip-installed]\n'
            f'  slpkg [{self.cyan}COMMAND{self.endc}] [update, upgrade, check-updates, clean-logs, clean-tmp]\n'
            f'  slpkg [{self.cyan}COMMAND{self.endc}] [-b, build, -i, install, -d, download] <packages>\n'
            f'  slpkg [{self.cyan}COMMAND{self.endc}] [-r, remove, -f, find, -w, view, -s, search] <packages>\n'
            "  \nIf you need more information please try 'slpkg --help'.")

        print(args)
        raise SystemExit()

    def help(self, status: int):
        args = [
            f'{self.bold}USAGE:{self.endc} {Configs.prog_name} [{self.yellow}OPTIONS{self.endc}] [{self.cyan}COMMAND{self.endc}] <packages>\n',
            f'{self.bold}DESCRIPTION:{self.endc}',
            '  Packaging tool that interacts with the SBo repository.\n',
            f'{self.bold}COMMANDS:{self.endc}',
            f'  {self.red}update{self.endc}                        Update the package lists.',
            f'  {self.cyan}upgrade{self.endc}                       Upgrade all the packages.',
            f'  {self.cyan}check-updates{self.endc}                 Check for news on ChangeLog.txt.',
            f'  {self.cyan}clean-logs{self.endc}                    Clean dependencies log tracking.',
            f'  {self.cyan}clean-tmp{self.endc}                     Delete all the downloaded sources.',
            f'  {self.cyan}-b, build{self.endc} <packages>          Build only the packages.',
            f'  {self.cyan}-i, install{self.endc} <packages>        Build and install the packages.',
            f'  {self.cyan}-d, download{self.endc} <packages>       Download only the scripts and sources.',
            f'  {self.cyan}-r, remove{self.endc} <packages>         Remove installed packages.',
            f'  {self.cyan}-f, find{self.endc} <packages>           Find installed packages.',
            f'  {self.cyan}-w, view{self.endc} <packages>           View packages from the repository.',
            f'  {self.cyan}-s, search{self.endc} <packages>         Search packages from the repository.\n',
            f'{self.bold}OPTIONS:{self.endc}',
            f'  {self.yellow}--yes{self.endc}                         Answer Yes to all questions.',
            f'  {self.yellow}--jobs{self.endc}                        Set it for multicore systems.',
            f'  {self.yellow}--resolve-off{self.endc}                 Turns off dependency resolving.',
            f'  {self.yellow}--reinstall{self.endc}                   Upgrade packages of the same version.',
            f'  {self.yellow}--skip-installed{self.endc}              Skip installed packages.\n',
            '  -h, --help                    Show this message and exit.',
            '  -v, --version                 Print version and exit.\n',
            'Edit the configuration file in the /etc/slpkg/slpkg.toml.',
            'If you need more information try to use slpkg manpage.']

        for opt in args:
            print(opt)
        raise SystemExit(status)
