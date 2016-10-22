#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger('omnisharp')
# Setup logging to store stuff about the communication with the server
# logger.setLevel(logging.DEBUG)
# 
# log_dir = os.path.join(vim.eval('expand("<sfile>:p:h")'), '..', 'log')
# if not os.path.exists(log_dir):
#     os.makedirs(log_dir)
# hdlr = logging.FileHandler(os.path.join(log_dir, 'python.log'))
# logger.addHandler(hdlr)
# 
# formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
# hdlr.setFormatter(formatter)
