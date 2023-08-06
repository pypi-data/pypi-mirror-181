root_cmake_raw = """# Root
# cmake版本
cmake_minimum_required(VERSION 3.12)
# 项目名
project(ROOT_IMCA)
# C++ 版本
set(CMAKE_CXX_STANDARD 17)
# 编译模式
set(CMAKE_BUILD_TYPE Debug)
# clangd使用的
set(CMAKE_EXPORT_COMPILE_COMMANDS 1)
# 添加头文件目录
include_directories(${PROJECT_SOURCE_DIR}/pkg/)
# 搜索Python脚本
execute_process(COMMAND python3 find_sub.py WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}/script)
# 读取功能包列表
file(READ ${PROJECT_SOURCE_DIR}/script/ModuleList.txt read_file_var)
# Set Submodule BEGIN
set(Module_Lists ${read_file_var})
separate_arguments(Module_Lists)
foreach(sub_name IN LISTS Module_Lists)
	message(NOTICE SubModuleName: ${sub_name})
	message(NOTICE SubModulePath: ${PROJECT_SOURCE_DIR}/pkg/${sub_name})
	add_subdirectory(${PROJECT_SOURCE_DIR}/pkg/${sub_name})
endforeach()
# Set Submodule END
# 查找当前目录下的SRC文件
aux_source_directory(. DIR_SRCS)
# 添加到可执行文件
add_executable(${PROJECT_NAME} ${DIR_SRCS})
# Third Model BEGIN
foreach(sub_name IN LISTS Module_Lists)
	string(FIND ${sub_name} "/" sub_pos REVERSE)
	if(${sub_pos} GREATER -1)
		math(EXPR sub_pos "${sub_pos} + 1" OUTPUT_FORMAT DECIMAL)
		message(Sub_Pos: ${sub_pos})
		string(SUBSTRING ${sub_name} ${sub_pos} -1 sub_name)
	endif()
	target_link_libraries(${PROJECT_NAME} ${sub_name})
endforeach()
# Third Model END
# 从此处自定义连接第三方库
"""