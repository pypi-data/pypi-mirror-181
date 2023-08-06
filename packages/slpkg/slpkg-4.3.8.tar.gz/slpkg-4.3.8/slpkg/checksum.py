#!/usr/bin/python3
# -*- coding: utf-8 -*-


import hashlib

from slpkg.views.views import ViewMessage


class Md5sum:
    """ Checksum the sources. """

    def __init__(self, flags):
        self.flags = flags

    def check(self, path: str, source: str, checksum: str, name: str):
        filename = f'{path}/{source.split("/")[-1]}'

        md5 = self.read_file(filename)

        file_check = hashlib.md5(md5).hexdigest()

        if file_check not in checksum:
            print('\nExpected:', ''.join(checksum))
            print('Found:', file_check)
            print(f'\nMD5SUM check for {name} FAILED.')

            view = ViewMessage(self.flags)
            view.question()

    @staticmethod
    def read_file(filename: str):
        with open(filename, 'rb') as f:
            return f.read()
