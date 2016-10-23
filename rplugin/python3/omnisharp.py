#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Main module, which is used by omnisharp-vim
'''

import logging
import subprocess
from os import path
from enum import Enum
from glob import glob

import neovim

logger = logging.getLogger('omnisharp')
# Setup logging to store stuff about the communication with the server
# logger.setLevel(logging.DEBUG)
#
# log_dir = path.join(vim.eval('expand("<sfile>:p:h")'), '..', 'log')
# if not path.exists(log_dir):
#     os.makedirs(log_dir)
# hdlr = logging.FileHandler(path.join(log_dir, 'python.log'))
# logger.addHandler(hdlr)
#
# formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
# hdlr.setFormatter(formatter)

class ServerType(Enum):
    '''Enumeration for storring possible ways to use the OmniSharp server'''
    mono = "v1"
    roslyn = "roslyn"
    roslyn_mono = "roslyn_mono"

@neovim.plugin
class OmniSharp(object):
    '''Main plugin, which is responsible for main tasks, like communicating
    with the server.
    '''

    default_port = 2000
    plugin_root = path.abspath(path.join(path.dirname(__file__), "..", ".."))

    def __init__(self, nvim):
        self.vim = nvim
        self.server_type = ServerType.mono
        self.proc = None

    @property
    def port(self):
        '''Get port for the omnisharp server'''
        return self.default_port

    @property
    def server_path(self):
        '''Get the OmniSharp server path'''
        if self.server_type == ServerType.mono:
            return path.join(self.plugin_root, "server", "OmniSharp", "bin",
                             "Debug", "OmniSharp.exe")
        elif self.server_type == ServerType.roslyn:
            return path.join(self.plugin_root, "omnisharp-roslyn", "artifacts",
                             "scripts", "OmniSharp")

    @property
    def solution_name(self):
        '''Get the OmniSharp server path'''
        if self.server_type == ServerType.mono:
            return "*.sln"
        elif self.server_type == ServerType.roslyn:
            return "project.json"

    @property
    def pwd(self):
        '''Get the current filename.'''
        current_dir = path.dirname(self.vim.current.buffer.name)

    def discover_solution_files(self):
        '''Get all of the solution files we can find'''
        current_dir = self.pwd
        solution_files = []
        while len(solution_files) == 0:
            p = path.join(current_dir, self.solution_name)
            solution_files = list(glob(p))

            print(p)
            if solution_files:
                solution_files = list(solution_files)
                break

            tmp = path.abspath(path.join(current_dir, ".."))
            if tmp == current_dir:
                break
            current_dir = tmp

        return solution_files

    @property
    def solution_path(self):
        '''Finds the solution path'''
        solution_files = self.discover_solution_files()
        # FIXME: prompt a dialog for more than one solution
        selected_solution = solution_files[0]
        return selected_solution

    @neovim.command("OmniSharpStartServer")
    def start_server(self):
        '''Starts the omnisharp server as described in documentation.

        https://github.com/OmniSharp/omnisharp-roslyn/blob/dev/doc/Using-Omnisharp.md

        TODO:
        - support for `--hostPID` option.
        - support for `--stdio` option.
        - support for autodetecting solution.

        The benefits of having this were outlined here:
        https://github.com/OmniSharp/omnisharp-vim/issues/215
        '''
        if self.proc is not None:
            self.proc = subprocess.Popen([
                "sh", "-c", self.server_path, "-p", self.port, self.solution_path])
        else:
            logger.info("Server is already running")

    @neovim.command("OmniSharpStopServer")
    def stop_server(self):
        '''Starts the omnisharp server as described in documentation.

        https://github.com/OmniSharp/omnisharp-roslyn/blob/dev/doc/Using-Omnisharp.md

        TODO:
        - support for `--hostPID` option.
        - support for `--stdio` option.
        - support for autodetecting solution.

        The benefits of having this were outlined here:
        https://github.com/OmniSharp/omnisharp-vim/issues/215
        '''
        raise NotImplementedError
