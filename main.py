'''
Author: xuranXYS
LastEditTime: 2023-06-27 22:49:39
GitHub: www.github.com/xiaoxustudio
WebSite: www.xiaoxustudio.top
Description: By xuranXYS
'''
import io
import sys,os
import xs.Expresstion

# test=""
# # 创建解释器
# exp=xs.Expresstion.xExp()

# with open("./a.xs",encoding="utf-8") as file:
#     test=file.read()
#     file.close()


# exp.execute(test,func="main")





def main():
    for i in range(1, len(sys.argv)):
        if sys.argv[i].startswith("-"):
            # 命令参数
            return 0
        else:
            test=""
            # 创建解释器
            exp=xs.Expresstion.xExp()
            with open(sys.argv[i],encoding="utf-8") as file:
                test=file.read()
                file.close()
            exp.execute(test)
            


if __name__ == "__main__":
    main()







