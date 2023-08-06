import yaml

from imca_tools.command.base_var import *
from imca_tools.logger.logger import Logger

def create_yaml(m_name, mode):

    if(str(m_name).find("/") == 0):
        m_name = m_name[1:]

    if(mode == YAML_MODE.ROOT):
        yaml_type = "root"
    elif(mode == YAML_MODE.PKG):
        yaml_type = "pkg"

    info_data = {
        "module_name": m_name,
        "author": pwd.getpwuid( os.getuid())[0],
        "create_time": now_time,
        "type" : yaml_type,
        "descripe": ""
    }

    if(mode == YAML_MODE.ROOT):
        with open(cur_path + "/." + "Config" + ".yaml", "w", encoding="utf-8") as f:
            yaml.dump(data=info_data, stream=f, allow_unicode=True)
            Logger.INFO_NOTE("创建根YAML")
    elif(mode == YAML_MODE.PKG and RM_PATH is not None):
        with open(RM_PATH + "/pkg/" + m_name + "/." + "Config" + ".yaml", "w", encoding="utf-8") as f:
            yaml.dump(data=info_data, stream=f, allow_unicode=True)
            Logger.INFO_NOTE("成功创建功能包YAML")
    pass