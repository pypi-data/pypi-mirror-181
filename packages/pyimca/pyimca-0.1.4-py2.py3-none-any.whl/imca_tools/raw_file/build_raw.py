build_raw = """#! /bin/bash

if [ ! -d "./vs-build" ]; then
    mkdir ./vs-build
fi

cd ./vs-build

title='[ EXECUTE ]'

python3 ../script/find_sub.py

cmake -DCMAKE_CXX_COMPILER=/usr/bin/clang++ -DCMAKE_C_COMPILER=/usr/bin/clang .. && make -j12

if [ $? -eq 0 ]; then
    clear
    yes "=" | sed '5q' | tr -d '\\n'
    echo -n ${title}
    yes "=" | sed '5q' | tr -d '\\n'
    echo ''
    echo ''
    ./ROOT_IMCA
fi

"""