pkg_cmake_pkg = """
# 功能包名
project("{0}")
# 搜索.cpp文件的所有路径
FILE(GLOB_RECURSE CPP_SET ${{PROJECT_SOURCE_DIR}} *.cpp)
# 搜索.h文件的所有路径
FILE(GLOB_RECURSE H_SET ${{PROJECT_SOURCE_DIR}} *.h)
message(NOTICE "SRC_SET = " ${{CPP_SET}})
message(NOTICE "H_SET = " ${{H_SET}})
message(NOTICE )
# 添加头文件路径
include_directories(${{PROJECT_SOURCE_DIR}}/include/)
include_directories(${{PROJECT_SOURCE_DIR}}/interface/)
# 添加子包
add_library(${{PROJECT_NAME}} ${{CPP_SET}} ${{H_SET}})
"""