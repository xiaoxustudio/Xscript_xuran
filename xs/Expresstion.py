'''
Author: xuranXYS
LastEditTime: 2023-06-22 12:24:49
GitHub: www.github.com/xiaoxustudio
WebSite: www.xiaoxustudio.top
Description: By xuranXYS
'''
# 解释器
import re
import enum


class TypeS(enum.Enum):
    caozuofu=1
    biaodashi=2
    hanshu=3
    # 字符串
    zfc=4

# 存放命名空间
F_Space={
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
                        print(er.args[0],er.args[1])                
                            
                
                
                
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
                    n_te=i.replace(" ","")
                    if F_Space["main"]["main()"]["sub"][n_te]=="None":
                        n_pos.append(n_te)
                        if ";" in n_te:
                            if xExp_type().execute(n_te)==TypeS.hanshu:
                                xExp_F(n_te)
                        elif not n_te in bds_list:
                            # 不是表达式操作符则报错
                            raise ErrorM(["Error","表达式错误"])
                    
                return n_pos
            except ValueError:
                return ["Error","括号前有未知标识符"]
            except ErrorM as e:
                print(e.args[0]+":"+e.args[1])



function_list={
    "tw":print
}
# 函数执行器
class XFunc:
    def tw(self,*args):
        for i in args:
            print(i)
    def execute(self,text:str,ar:list):
        try:
            for i in ar:
                eval("self."+text+"("+str(i)+")")
        except Exception as error:
            return ["Error","函数解析错误"]
            




# 函数解析器
class xExp_F:
    def __init__(self,text):
        # 函数标识
        e_pos :str=re.sub(r'\s+', ')', text[:text.rindex('(')] )
        e_pos_args :str=re.findall(r'\((.*?)\)', text[text.index('('):])[0]
        try:
            XFunc().execute(e_pos,e_pos_args.split(","))
        except Exception as error:
            return ["Error","出现异常错误"]





# 类型解析器
class xExp_type:
    def execute(selfl,text:str) -> None:
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
        else:
            # 操作符
            return TypeS.caozuofu
        




