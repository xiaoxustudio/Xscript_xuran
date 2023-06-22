'''
Author: xuranXYS
LastEditTime: 2023-06-22 12:34:55
GitHub: www.github.com/xiaoxustudio
WebSite: www.xiaoxustudio.top
Description: By xuranXYS
'''
import io
import sys,os
import xs.Expresstion
import xs.Func
test=""

# 创建解释器
exp=xs.Expresstion.xExp()

with open("./a.xs",encoding="utf-8") as file:
    test=file.read()
    file.close()

exp.execute(test)


