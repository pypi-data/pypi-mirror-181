import fire
import os
import yaml
import sys

from imca_tools.raw_file.help_raw import help
from imca_tools.logger.logger import Logger
from imca_tools.command.workspace import create_workspace
from imca_tools.command.pkg import package
from imca_tools.command.list_pkg import list_pkg_fun

class imca:
    def help(self):
        print(help)

    def list_pkg(self):
        list_pkg_fun()

    class create:
        def workspace(self, type):
            Logger.INFO_NOTE("创建工作空间")
            if(create_workspace(type) == 0):
                Logger.INFO_SUCC("创建工作空间成功")
            else:
                Logger.INFO_ERR("创建工作空间失败")
            pass

        def pkg(self, name):
            Logger.INFO_NOTE("创建功能包 {0}".format(name))
            if(package(name) == 0):
                Logger.INFO_SUCC("创建功能包成功")
            else:
                Logger.INFO_ERR("创建功能包失败")
            pass
    pass

def main():
    fire.Fire(imca)

if __name__ == '__main__':
    main()