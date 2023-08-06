from imca_tools.command.find_sub import find_yaml
from imca_tools.command.base_var import *
from imca_tools.logger.logger import Logger

import yaml

def list_pkg_fun():
    if(RM_PATH is None):
        Logger.INFO_ERR("环境不存在")
        return -1

    yaml_list = find_yaml(RM_PATH)
    for cur_file in yaml_list:
        yaml_file = cur_file
        with open(yaml_file, "r", encoding="utf-8") as f:
            result = yaml.load(f.read(), Loader=yaml.FullLoader)
            print("包名 : %s\t\t作者 : %s\t\t创建时间 : %s\t\t描述 : %s\n\t>>> 所在路径 : %s" %(result["module_name"], result["author"], result["create_time"], result["descripe"], yaml_file))
            print("------------------------------------------------------")

    return 0
    pass
