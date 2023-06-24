'''
Author: xuranXYS
LastEditTime: 2023-06-24 14:13:38
GitHub: www.github.com/xiaoxustudio
WebSite: www.xiaoxustudio.top
Description: By xuranXYS
'''
# 解释器
import re
import enum
import ast
import os, sys
current_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(current_dir)
# 导入内置函数库
from Func import *


class TypeS(enum.Enum):
    caozuofu=1
    biaodashi=2
    hanshu=3
    # 字符串
    zfc=4

# 存放命名空间
F_Space={
}

# 文件全局隐私变量命名空间
T_Space={
    "global":{},
    "local":{}
}



# 表达式操作符
bds_list=["{","}","(",")",";"]



# 异常错误管理器
class ErrorM(ReferenceError):
    def __init__(self, arg):
        self.args = arg

# 表达式解析器
class xExp:
    def execute(self,text):
        text=str(text)
        # 表达式是否符合规则
        if text.count("{")==text.count("}"):
            # 截取括号之前的函数名称
            try:
                # 使用正则表达式匹配并替换每行中的注释内容
                pattern = r"//.*"
                text = re.sub(pattern, "", text)
                #按照嵌套截取{}
                # 记录需要处理的括号数量
                left_count=0
                # 寻找次数：如果寻找括号等于括号数量，那么括号嵌套就找完了，每次找到一对{}，就会记录一次
                find_num=0
                # 最后索引位置：下次执行寻找就从这开始找
                last_index=0
                def find_parse(text,j_type="hs",hanshuname=None):
                    nonlocal find_num
                    nonlocal left_count
                    all_stack={}
                    try:
                        match j_type:
                            case "hs":
                                # 截取函数名称
                                hanshu_name=re.sub(r'\s+', '', text[text.find('fc')+2:text.find('{')])
                                name_qu_text=text.replace(text[text.find('fc'):text.find('{')], '')
                                nested_dict={}
                                stack_dict={}
                                stack=[]
                                stack1=[]
                                q_text=re.sub(r'\s+', '', name_qu_text)
                                # 寻找到的{的次数
                                find_right_num=0
                                for i, c in enumerate(q_text):
                                    if c=="{":
                                        stack.append(i)
                                        stack_dict[hanshu_name]={"index":i,"sub":"null"}
                                    elif c=="}":
                                        stack1.append(i)
                                        #记录需要处理括号的数量
                                        if left_count==0 :left_count=len(stack)
                                        # 弹出最上面的左大括号
                                        left_bracket_index = stack.pop()
                                        # 获取当前右大括号前面的子串
                                        substring = re.sub(r'\s+', '', q_text[left_bracket_index+1:i])
                                        # 判断是否还有{
                                        if substring.count("{"):
                                            # 递归调用函数获取子串中的嵌套大括号内容
                                            nested_dict[substring[:substring.find("{")]] = {
                                                "index":left_bracket_index,
                                                "sub":find_parse(substring,j_type="con",hanshuname=hanshu_name)
                                            }
                                        else:
                                            for i in substring.split(";"):
                                                i=re.sub(r'\s+', ')', i)
                                                if not i=="":
                                                    nested_dict[i+";"]="None"
                                            stack_dict[hanshu_name]={"index":stack_dict[hanshu_name]["index"],"sub":nested_dict}
                                        
                                        find_num+1#记录一次处理大括号
                                
                                return stack_dict
                            case "con":
                                nested_dict={}
                                stack_dict={}
                                stack=[]
                                stack1=[]
                                q_text=re.sub(r'\s+', '', text)
                                for i, c in enumerate(q_text):
                                    if c=="{":
                                        stack.append(i)
                                        stack_dict[hanshuname]={"index":i,"sub":"null"}
                                    elif c=="}":
                                        stack1.append(i)
                                        # 弹出最上面的左大括号
                                        left_bracket_index = stack.pop()
                                        # 获取当前右大括号前面的子串
                                        substring = re.sub(r'\s+', '', q_text[left_bracket_index+1:i])
                                        # 判断是否还有}
                                        if substring.count("{"):
                                            # 递归调用函数获取子串中的嵌套大括号内容
                                            nested_dict[substring[:substring.find("{")]] = {
                                                "index":left_bracket_index,
                                                "sub":find_parse(substring,j_type="con",hanshuname=hanshu_name)
                                            }
                                        else:
                                            for i in substring.split(";"):
                                                i=re.sub(r'\s+', ')', i)
                                                if not i=="":
                                                    nested_dict[i+";"]="None"
                                            stack_dict[hanshuname]={"index":stack_dict[hanshuname]["index"],"sub":nested_dict}
                                        
                                        find_num+1#记录一次处理大括号
                                return nested_dict
                    except ErrorM as er:
                        print(er.args[0]+"：\n"+er.args[1])                
                            
                
                
                
                # 通过正则表达式匹配 fc *(){}
                pattern = r"fc\s+\w+\s*\(.*?\)\s*\{(?:\{.*?\}|.)*?\}"
                regex = re.compile(pattern, re.DOTALL)
                matches = regex.findall(text)
                
                # 将匹配结果存储在字典中
                result_dict = {}
                for match in matches:
                    # 获取函数名
                    name = re.search(r"fc\s+(\w+)\s*\(", match).group(1)
                    # 存储到字典中
                    result_dict[name] = match.strip()
                
                for name, content in result_dict.items():
                    allstr=find_parse(content,j_type="hs")
                    # 将截取的内容添加进空间
                    F_Space[name]=allstr
                n_pos=[]
                # 运行main里面的代码
                for i in F_Space["main"]["main()"]["sub"]:
                    #如果不是变量则替换空行
                    if i.startswith("local",0) or i.startswith("global",0):
                        n_te=i.replace("local","local@")
                        n_te=n_te.replace("global","global@")
                    else:
                        n_te=i.replace(" ","")
                    if F_Space["main"]["main()"]["sub"][n_te.replace("@","")]=="None":
                        n_pos.append(n_te)
                        if ";" in n_te:
                            if xExp_type().execute(n_te)==TypeS.hanshu:
                                xExp_F(n_te)
                            elif xExp_type().execute(n_te)==TypeS.biaodashi:
                                XExp_sub(n_te)
                        elif not n_te in bds_list:
                            # 不是表达式操作符则报错
                            raise ErrorM(["Error",self.__class__.__name__+"：表达式错误"])
                    
                return n_pos
            except ValueError:
                return ["Error","括号前有未知标识符"]
            except ErrorM as e:
                print(e.args[0]+":\n"+e.args[1])

# 内置函数库
function_list={
    "tw":"self",
    "Space":"other",
}


# 函数执行器
class XFunc(Func):
    def tw(self,*args,show_type=1):
        for i in args:
            # 隐私变量首先判断
            if show_type==3 and args[0].startswith("$"):
                try:
                    res=str(args[0]).replace("$","")
                    print(res)
                    if res in T_Space:
                        print(T_Space[res])
                    else:
                        raise ErrorM(["Error",self.__class__.__name__+"：内置变量无法找到"])
                    return 0
                except ErrorM as e:
                    print(e.args[0]+":\n"+e.args[1])
                    return 0
            variables = dict(T_Space["global"],**T_Space["local"])
            # 将不是字符串的字母替换成数值
            pattern = r'[a-zA-Z_]\w*'
            variable_names = re.findall(pattern, i)
            # 替换内容2中的变量名为对应的值
            for name in variable_names:
                if name in variables:
                    # 判断是否是数字
                    pattern = r'^[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?$'
                    i = i.replace(name, str(variables[name]))
                    if bool(re.match(pattern, i)):
                        # 是数字
                        show_type=1
                    else:
                        show_type=2
            match show_type:
                case 1:
                    # 类型判断
                    leixing=xExp_type().execute(str(i),switch_t=2)
                    
                    match leixing:
                        case TypeS.zfc:
                            print(i)
                            break
                        case TypeS.hanshu:
                            print(eval("self."+str(i)))
                            break
                    break
                case 2:
                    # 运算
                    print(eval(str(i)))
                    break
                
    def execute(self,text:str,ar:list):
        try:
            for i in ar:
                # 判断是否是字符串类型
                if str(i).find("\"",0)!=-1 and str(i).find("\"",len(str(i))-1)!=-1 or str(i).find("\'",0)!=-1 and str(i).find("\'",len(str(i))-1)!=-1:
                    eval("self."+text+"("+str(i)+")")
                elif i in T_Space["global"] or i in T_Space["local"]:
                    res = T_Space["global" if i in T_Space["global"] else "local"][i]
                    eval("self."+text+"("+str(res)+")")
                elif str(i).startswith("$"):
                    # 隐私变量
                    eval("self."+text+"(\""+str(i)+"\",show_type=3)")
                elif ast.parse(str(i)):
                    # 表达式解析
                    eval("self."+text+"(\""+str(i)+"\")")
                else:
                    raise ErrorM(["Error",self.__class__.__name__+"：函数执行表达式异常字符错误"])
        except ErrorM as e:
            print(e.args[0]+":\n"+e.args[1])
            


# 内表达式解析器
class XExp_sub:
    def __init__(self,text) -> TypeS:
        try:
            # 使用正则表达式匹配目标内容
            pattern = r"([^@]+)@([^=]+)=([^;]+);"
            matches = re.findall(pattern, text)
            # 输出结果
            for match in matches:
                left = match[0].strip()
                middle = match[1].strip()
                ast.parse(match[2].strip())
                right = re.sub(r'\s+', '', match[2].strip())
                
                leixing=xExp_type().execute(str(right),switch_t=2)
                match leixing:
                    case TypeS.zfc:
                        # 是否是表达式
                        if right.startswith("\"") and right.endswith("\""):
                            # 加入到全局存储表里面
                            T_Space[left][middle]="\""+str(right)[1:len(right)-1]+"\""
                        else:
                            # 加入到全局存储表里面
                            T_Space[left][middle]=eval(str(right))
                        break
                    case TypeS.hanshu:
                        # 加入到全局存储表里面
                        T_Space[left][middle]=eval(str(right))
                        break
                
        except SyntaxError:
            raise ErrorM(["Error",self.__class__.__name__+"：无效的语法错误"])




# 函数解析器
class xExp_F:
    def __init__(self,text:str):
        try:
            # 函数标识
            
            # 匹配左括号
            pattern_left = r".*?\("
            pattern_right = r"\)"
            
            # 以下都是返回位置索引:匹配首次（）
            left = re.match(pattern_left,text).span()[1]
            right = list(re.finditer(pattern_right, text))[-1].start()
            
            
            e_pos :str=re.sub(r'\s+', "", text[:left-1])
            e_pos_args :str=text[left:right]
            
            XFunc().execute(e_pos,e_pos_args.split(","))
        except Exception as error:
            raise ErrorM(["Error",self.__class__.__name__+"：函数解析异常错误"])






# 类型解析器
class xExp_type:
    '''
    description: 
    param {*} selfl
    param {str} text
    param {*} switch_t 有无;号
    return {*}
    '''
    def execute(selfl,text:str,switch_t=1) -> None:
        match switch_t:
            case 1:
                if(text.endswith(");")):
                    # 类型可能是函数
                    res=text[:text.find("(")]
                    if(res):
                        return TypeS.hanshu
                    else:
                        return TypeS.zfc
                elif(text.endswith(";")):
                    # 类型可能是表达式或函数
                    return TypeS.biaodashi
                elif text in bds_list:
                    # 操作符
                    return TypeS.caozuofu
                else:
                    # 字符串
                    return TypeS.zfc
            case 2:
                if(text.endswith(")")):
                    # 类型可能是函数
                    res=text[:text.find("(")]
                    if(res):
                        return TypeS.hanshu
                    else:
                        return TypeS.zfc
                elif(text.endswith(")")):
                    # 类型可能是表达式或函数
                    return TypeS.biaodashi
                elif text in bds_list:
                    # 操作符
                    return TypeS.caozuofu
                else:
                    # 字符串
                    return TypeS.zfc
                    
        




