import re
pat="[a-zA-Z_]\w*"
x=input("请输入一个标识符：")
if re.match(pat,x):
    print("正确！")
else:
    print("错误！")