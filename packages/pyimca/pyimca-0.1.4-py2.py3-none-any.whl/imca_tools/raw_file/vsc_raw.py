task_raw = """
{
    "version": "2.0.0",
    "options": {
        "cwd": "${workspaceRoot}"
    },//指定命令执行所在路径
    "tasks": [
        {
            "label": "run",
            "type": "shell",
            "command": "bash ./script/build.sh",
            "args": [],
            "problemMatcher": [],
            "group": {
                "kind": "build",
                "isDefault": true
            }
        }
    ]
}

"""

launch_raw = """
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [

        {
            "type": "lldb",
            "request": "launch",
            "name": "Debug",
            "program": "${workspaceFolder}/vs-build/ROOT_IMCA",
            "args": [],
            "cwd": "${workspaceFolder}"
        }
    ]
}
"""