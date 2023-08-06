# -*- coding: UTF-8 -*-

import os
import yaml

from imca_tools.logger.logger import Logger
from imca_tools.command.base_var import *
from imca_tools.command.find_sub import find_sub
from imca_tools.command.yame_build import create_yaml
from imca_tools.raw_file.pkg_src_raw import pkg_src_raw
from imca_tools.raw_file.pkg_inc_raw import pkg_inc_raw
from imca_tools.raw_file.impl_inc_raw import impl_inc_raw
from imca_tools.raw_file.impl_src_raw import impl_src_raw
from imca_tools.raw_file.pkg_cmake_raw import pkg_cmake_pkg

# 这个将会在../pkg下进行
def package(pname):
    if(RM_PATH is None):
        Logger.INFO_ERR("无对应环境RM_PATH, 请source环境")
        return -1


    for sub_file in find_sub(RM_PATH + "/pkg"):
        if(pname in sub_file):
            Logger.INFO_ERR("功能包名重复")
            return -2

    # if(len(find_sub(RM_PATH + "/pkg")) > 0):
    #     Logger.INFO_ERR("功能包名重复")
    #     return -2

    for yaml_file in find_sub(RM_PATH + "/pkg"):
        if(yaml_file in cur_path):
            Logger.INFO_ERR("不能在功能包中创建功能包")
            return -3

    if((RM_PATH + "/pkg") not in cur_path):
        Logger.INFO_ERR("不再当前工作空间")
        return -4

    pkg_path = cur_path + "/" + pname
    src_path = pkg_path + "/source"
    impl_path = pkg_path + "/interface"
    inc_path = pkg_path + "/include"

    os.mkdir(pkg_path)
    Logger.INFO_NOTE("创建功能包文件")
    os.mkdir(src_path)
    os.mkdir(impl_path)
    os.mkdir(inc_path)
    Logger.INFO_NOTE("创建 资源包 头文件包 接口包")
    src_file_name = src_path + "/" + pname + ".cpp"
    inc_file_name = inc_path + "/" + pname + ".h"
    impl_inc_file_name = impl_path + "/" + pname + "_impl.h"
    impl_src_file_name = impl_path + "/" + pname + "_impl.cpp"
    cmake_file_path = pkg_path + "/CMakeLists.txt"

    src_file = open(src_file_name, "w")
    src_file.write(pkg_src_raw.format(author, pname))
    src_file.close()

    inc_file = open(inc_file_name, "w")
    inc_file.write(pkg_inc_raw.format(author, pname.upper(), pname))
    inc_file.close()

    impl_inc_file = open(impl_inc_file_name, "w")
    impl_inc_file.write(impl_inc_raw.format(author, pname.upper(), pname))
    impl_inc_file.close()

    impl_src_file = open(impl_src_file_name, "w")
    impl_src_file.write(impl_src_raw.format(author, pname))
    impl_src_file.close()
    Logger.INFO_NOTE("创建原始文件")

    cmake_file = open(cmake_file_path, "w")
    cmake_file.write(pkg_cmake_pkg.format(pname))
    cmake_file.close()
    Logger.INFO_NOTE("创建子cmake")

    yaml_file = cur_path[len(RM_PATH+"/pkg")+1:] + "/" + pname
    #print(yaml_file)
    create_yaml(yaml_file, YAML_MODE.PKG)
    return 0
    pass