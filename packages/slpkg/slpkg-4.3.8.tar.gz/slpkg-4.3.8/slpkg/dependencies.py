#!/usr/bin/python3
# -*- coding: utf-8 -*-


from slpkg.queries import SBoQueries


class Requires:
    """ Creates a list of dependencies with
    the right order to install. """

    def __init__(self, name):
        self.name = name

    def resolve(self) -> list:
        requires = SBoQueries(self.name).requires()

        for req in requires:
            if req:
                sub = SBoQueries(req).requires()
                for s in sub:
                    requires.append(s)

        requires.reverse()

        return list(dict.fromkeys(requires))
