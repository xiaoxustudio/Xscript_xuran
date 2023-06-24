'''
Author: xuranXYS
LastEditTime: 2023-06-24 15:10:03
GitHub: www.github.com/xiaoxustudio
WebSite: www.xiaoxustudio.top
Description: By xuranXYS
'''
import io
import sys,os
import xs.Expresstion

# test=""
# s=input("")
# # 创建解释器
# exp=xs.Expresstion.xExp()

# with open(s,encoding="utf-8") as file:
#     test=file.read()
#     file.close()


# exp.execute(test)





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







