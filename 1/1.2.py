import re
file="bracketed.txt"
with open(file,'r',encoding='utf-8') as rf:
    data=rf.read()
pat="(\w{2} [^()]{1,})"
result=re.compile(pat).findall(data)
for i in result:
    temp=i.split()
    print(temp[1]+'/'+temp[0],end=' ')