#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Unit tests for the new neovim plugin'''

import os
from unittest.mock import PropertyMock
from unittest.mock import patch
from omnisharp import OmniSharp

def test_plugin_root():
    '''Test that we can find the OmniSharp server submodule in the root of the
    directory'''
    for i in ["server", "plugin"]:
        assert os.path.exists(os.path.join(OmniSharp.plugin_root, i))

def test_mono_server_path():
    '''Test that we can get the path correctly for the OmniSharp server'''
    osharp = OmniSharp(None)
    assert osharp.server_path.endswith(os.path.join(
        "server", "OmniSharp", "bin", "Debug", "OmniSharp.exe"))

@patch('omnisharp.OmniSharp.solution_name', new_callable=PropertyMock)
@patch('omnisharp.OmniSharp.pwd', new_callable=PropertyMock)
def test_discover_solution_file(mock_pwd, mock_solution_name):
    '''Test that we can discover the OmniSharp server solution file.'''
    mock_pwd.return_value = os.path.join(
        OmniSharp.plugin_root, "server", "OmniSharp", "AutoComplete")
    mock_solution_name.return_value = "*.sln"

    osharp = OmniSharp(None)
    assert osharp.solution_name == "*.sln"
    assert osharp.discover_solution_files()[0].endswith(
        os.path.join("server", "OmniSharp.sln"))
