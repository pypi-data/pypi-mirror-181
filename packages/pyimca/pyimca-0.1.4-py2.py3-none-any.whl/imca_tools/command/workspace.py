# -*- coding: UTF-8 -*-

import os
import stat
import yaml


from imca_tools.logger.logger import Logger
from imca_tools.command.base_var import *
from imca_tools.raw_file.main_raw import main_raw
from imca_tools.command.yame_build import create_yaml
from imca_tools.raw_file.build_raw import build_raw
from imca_tools.raw_file.clang_format_raw import clang_format_raw
from imca_tools.raw_file.clang_raw import clang_raw
from imca_tools.raw_file.extensions_raw import extensions_raw
from imca_tools.raw_file.workspace_cmake_raw import root_cmake_raw
from imca_tools.raw_file.workspace_py_raw import search_py_raw
from imca_tools.raw_file.vsc_raw import *

def create_workspace(env_type):

    if(env_type != 'vsc' and env_type != 'clion'):
        Logger.INFO_ERR("错误的参数 " + env_type + ", type应该输入 vsc 或 clion ")
        return -3

    if(env_type == 'vsc'):
        Logger.INFO_NOTE("使用的IDE为 VScode")
    elif(env_type == 'clion'):
        Logger.INFO_NOTE("使用的IDE为 Clion")

    if(len(os.listdir(cur_path)) > 0):
        Logger.INFO_ERR("当前文件不为空")
        return -1

    if((RM_PATH != None) and RM_PATH in cur_path):
        Logger.INFO_ERR("无法在工作空间下重复创建工作空间")
        return -2

    # 工作包目录
    src_dir = cur_path + "/pkg"
    os.mkdir(src_dir)
    Logger.INFO_NOTE("创建工作包目录")

    # 脚本文件目录
    script_dir = cur_path + "/script"
    os.mkdir(script_dir)
    Logger.INFO_NOTE("创建脚本目录")

    # 主函数
    maincpp = open(cur_path + "/main.cpp", 'w')
    maincpp.write(author + "\n")
    maincpp.write(main_raw)
    maincpp.close()
    Logger.INFO_NOTE("创建main.cpp")

    # 启动脚本
    export_sh = open(script_dir + "/setup.sh", 'w')
    export_sh.writelines("unset RM_PATH\n")
    export_sh.writelines("export RM_PATH=" + cur_path)
    Logger.INFO_NOTE("创建启动脚本")
    export_sh.close()

    # 搜索脚本
    find_sub_py = script_dir + "/find_sub.py"
    find_sub_file = open(find_sub_py, "w")
    find_sub_file.write(search_py_raw.format(cur_path))
    find_sub_file.close()

    # 根Cmake
    cmake_file_path = cur_path + "/CMakeLists.txt"
    cmake_file = open(cmake_file_path, "w")
    cmake_file.write(root_cmake_raw)
    cmake_file.close()
    Logger.INFO_NOTE("创建根Cmake")

    if(env_type == 'vsc'):
        vscode_dir = cur_path + "/.vscode"
        os.mkdir(vscode_dir)
        Logger.INFO_NOTE("创建VSCODE目录")

        # 任务脚本
        task_json = open(vscode_dir + "/tasks.json", "w")
        task_json.write(task_raw)
        os.chmod(vscode_dir + "/tasks.json", stat.S_IREAD)
        Logger.INFO_NOTE("创建任务脚本")
        task_json.close()

        # Debug脚本
        launch_json = open(vscode_dir + "/launch.json", "w")
        launch_json.write(launch_raw)
        os.chmod(vscode_dir + "/launch.json", stat.S_IREAD)
        Logger.INFO_NOTE("创建Debug脚本")
        launch_json.close()

        # 编译脚本
        build_sh = open(script_dir + "/build.sh", "w")
        build_sh.write(build_raw)
        os.chmod(script_dir + "/build.sh", stat.S_IREAD)
        Logger.INFO_NOTE("创建编译脚本")
        build_sh.close()

        # 格式化脚本
        clang_format = open(cur_path + "/.clang-format", 'w')
        clang_format.write(clang_format_raw)
        Logger.INFO_NOTE("创建格式化脚本")
        clang_format.close()

        # clang配置文件
        clang = open(cur_path + "/.clangd", "w")
        clang.write(clang_raw)
        Logger.INFO_NOTE("创建clang配置文件")
        clang.close()

        # 扩展需求文件
        extension = open(cur_path + "/extensions.txt", "w")
        extension.write(extensions_raw)
        Logger.INFO_NOTE("创建扩展需求文件")
        extension.close()

    # 功能包列表
    sub_pkg = open(script_dir + "/ModuleList.txt", "w")
    Logger.INFO_NOTE("创建功能包列表")
    sub_pkg.close()

    create_yaml("root", YAML_MODE.ROOT)
    return 0
    pass


