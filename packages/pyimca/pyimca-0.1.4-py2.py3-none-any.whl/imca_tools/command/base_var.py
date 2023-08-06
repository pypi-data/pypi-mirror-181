# -*- coding: UTF-8 -*-

import sys
import os
import datetime as dt
import pwd

from enum import Enum

class YAML_MODE(Enum):
    ROOT = 1
    PKG = 2

class ENV_MODE(Enum):
    VSCODE = 1
    CLION = 2

cur_path = os.getcwd() # 当前终端位置
author = "// create by " + pwd.getpwuid( os.getuid())[0] + "\t " + str(dt.datetime.now().strftime('%F %T') + "\n") # 当前系统用户
RM_PATH = os.environ.get("RM_PATH") # 环境变量
now_time = str(dt.datetime.now().strftime('%F %T')) # 当前时间