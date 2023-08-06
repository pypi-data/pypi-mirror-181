pkg_inc_raw = """{0}
#ifndef {1}__H__
#define {1}__H__
#include <cstdio>

class {2}{{
private:
    // 存放私有变量

public:
    // 存放公共函数
    void to_string();
}};
#endif
"""