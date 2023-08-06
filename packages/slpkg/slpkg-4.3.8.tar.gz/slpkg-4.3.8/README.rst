.. contents:: Table of Contents:


About
-----

Slpkg is a software package manager that installs, updates and removes packages on `Slackware <http://www.slackware.com/>`_-based systems.
It automatically calculates dependencies and figures out what things need to happen to install packages. 
Slpkg makes it easier to manage groups of machines without the need for manual updates.

Slpkg works in accordance with the standards of the `SlackBuilds.org <https://www.slackbuilds.org>`_ organization to build packages. 
It also uses the Slackware Linux instructions for installing, upgrading or removing packages.

.. image:: https://gitlab.com/dslackw/images/raw/master/slpkg/slpkg_package.png
    :target: https://gitlab.com/dslackw/slpkg


Requirements
------------

.. code-block:: bash

    SQLAlchemy >= 1.4.36
    toml >= 0.10.2

Install
-------

Install from the official third-party `SBo repository <https://slackbuilds.org/repository/15.0/system/slpkg/>`_ or directly from source:

.. code-block:: bash

    $ tar xvf slpkg-4.3.8.tar.gz
    $ cd slpkg-4.3.8
    $ ./install.sh


Usage
-----

.. code-block:: bash

    $ slpkg --help

      USAGE: slpkg [OPTIONS] [COMMAND] <packages>

      DESCRIPTION:
        Packaging tool that interacts with the SBo repository.

      COMMANDS:
        update                        Update the package lists.
        upgrade                       Upgrade all the packages.
        check-updates                 Check for news on ChangeLog.txt.
        clean-logs                    Clean dependencies log tracking.
        clean-tmp                     Deletes all the downloaded sources.
        -b, build <packages>          Build only the packages.
        -i, install <packages>        Build and install the packages.
        -d, download <packages>       Download only the scripts and sources.
        -r, remove <packages>         Remove installed packages.
        -f, find <packages>           Find installed packages.
        -w, view <packages>           View packages from the repository.
        -s, search <packages>         Search packages from the repository.

      OPTIONS:
        --yes                         Answer Yes to all questions.
        --jobs                        Set it for multicore systems.
        --resolve-off                 Turns off dependency resolving.
        --reinstall                   Upgrade packages of the same version.
        --skip-installed              Skip installed packages.

        -h, --help                    Show this message and exit.
        -v, --version                 Print version and exit.

      If you need more information try to use slpkg manpage.


    $ slpkg install Flask
      The following packages will be installed or upgraded:

      [ install ] -> Flask-2.1.2

      Dependencies:
      [ install ] -> python-zipp-3.8.0
      [ install ] -> python-importlib_metadata-4.10.1
      [ install ] -> click-8.1.3
      [ install ] -> python3-itsdangerous-2.1.2
      [ install ] -> werkzeug-2.1.2

      Total 6 packages will be installed and 0 will be upgraded.

      Do you want to continue [y/N]:


      $ slpkg remove Flask
      The following packages will be removed:

      [ delete ] -> Flask-2.1.2-x86_64-1_SBo

      Dependencies:
      [ delete ] -> python-zipp-3.8.0-x86_64-2_SBo
      [ delete ] -> python-importlib_metadata-4.10.1-x86_64-1_SBo
      [ delete ] -> click-8.1.3-x86_64-1_SBo
      [ delete ] -> python3-itsdangerous-2.1.2-x86_64-1_SBo
      [ delete ] -> werkzeug-2.1.2-x86_64-1_SBo

      Total 6 packages will be removed.

      Do you want to continue [y/N]:


Configuration files
-------------------

.. code-block:: bash

    /etc/slpkg/slpkg.toml
        General configuration of slpkg

    /etc/slpkg/blacklist.toml
        Blacklist of packages

Donate
------

If you feel satisfied with this project and want to thanks me make a donation.

.. image:: https://gitlab.com/dslackw/images/raw/master/donate/paypaldonate.png
   :target: https://www.paypal.me/dslackw


Copyright
---------

- Copyright 2014-2022 © Dimitris Zlatanidis.
- Slackware® is a Registered Trademark of Patrick Volkerding. 
- Linux is a Registered Trademark of Linus Torvalds.
