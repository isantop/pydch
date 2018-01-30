#!/usr/bin/python3

"""
py2deb - Release a debian package based on a python distutils setup file.

Copyright 2018 Ian Santopietro <isantop@gmail.com>
"""

import logging, os, subprocess, shlex

class Py2Deb():

    current_directory = "/"
    setup_name = "setup.py"
    setup_path = "/setup.py"

    def __init__(self, args):
        self.args = args
        self.current_directory = os.getcwd()
        self.setup_path = os.path.join(current_directory, setup_name)

        logging.addLevelName(30, 'OUTPUT')

        self.log = logging.getLogger('py2deb')
        console = logging.StreamHandler()
        stream_fmt = logging.Formatter('%(name)-8s: %(levelname)-8s %(message)s')
        console.setFormatter(stream_fmt)
        self.log.addHandler(console)


    def main():

        verbosity = 0
        if args.verbose:
            verbosity = args.verbose
        if verbosity > 3:
            verbosity = 3

        level = {
            0 : 'ERROR
            1 : 'WARNING',
            2 : 'INFO',
            3 : 'DEBUG',
        }

        console_level = level[verbosity]
        self.log.setLevel(console_level)

        edit = False
        if args.edit:
            edit = True

        force = False
        if args.force_release:
            force = True

        distro = None
        if args.distro:
            distro = args.distro

        metadata = get_setup_lines(self.setup_path)

        version_command = 'dch -v %s' % metadata['version']
        edit_command = 'dch -e'
        release_command = 'dch -r ""'

        if edit:
            run_command(edit_command)
        else:
            run_command(version_command)
            run_command(release_command)

        return 0


    def run_command(self, command, simulate=True):
        if simulate = True:
            self.log.info("Simulating %s" % command)
        else:
            self.log.info('Running %s' command)
            command_list = shlex.split(command)
            subprocess.run(command_list, check=True)


    def get_setup_lines(self, path):
        setup_dict = {}
        with open(path, mode='r') as setup_file:
            for line in setup_file.readlines():
                if "=" in line:
                    setup_line = line.split('=')
                    setup_line[0] = clean_string(setup_line[0])
                    setup_line[1] = clean_string(setup_line[1])
                    setup_dict[setup_line[0]] = setup_line[1]

        return setup_dict


    def clean_string(self, string):
        remove_chars = {
            '\'' : '',
            '\"' : '',
            '\n' : '',
            ' '  : '',
            '('  : '',
            ','  : '',
            'setup' : '',
        }

        for char in remove_chars:
            string = string.replace(char, remove_chars[char])
            self.log.debug(string)

        return string
