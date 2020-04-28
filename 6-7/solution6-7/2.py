from collections import defaultdict


class MyClass:
    def __init__(self):
        self.numStart = 0  # 括号对开始位置
        self.numEnd = 0  # 括号对结束位置
        self.strPos = ''  # 该括号对所对应的句法规则符号
        self.strCluster = ''  # 该括号对直接包含的具体的词或标点符号


with open('train.bracketed.txt', 'r', encoding='utf-8') as fr:
    lines = fr.readlines()

brackets = []
for line in lines:
    line = line[2:-2]
    for i in range(len(line)):
        if line[i] == '(':
            a = MyClass()
            a.numStart = i
            a.numEnd = -1
            brackets.append(a)
        elif line[i] == ')':
            for j in range(len(brackets) - 1, -1, -1):
                if brackets[j].numEnd == -1:
                    brackets[j].numEnd = i
                    break
        elif line[i] == ' ':
            if line[i - 1] != ')':
                j = i - 1
                while line[j] != '(' and line[j] != ')':
                    j -= 1
                word = line[j + 1:i]
                brackets[-1].strPos = word
                if line[i + 1] != '(':
                    k = i + 1
                    while line[k] != '(' and line[k] != ')' and k < len(line):
                        k += 1
                    brackets[-1].strCluster = line[i + 1:k]

# 以下将每个产生式进行二叉化处理
N_dict = defaultdict(int)
NR_dict = defaultdict(int)
N_dict2 = defaultdict(int)
NR_dict2 = defaultdict(int)

production = []     #存取抽取出来的产生式及其概率
production2 = []    #存取抽取出来的产生式二叉化后的结果及其相应概率
for n in range(len(brackets)):
    numA = brackets[n].numStart
    numB = brackets[n].numEnd
    father = brackets[n].strPos
    N_dict[father] += 1
    N_dict2[father] += 1
    if brackets[n].strCluster != '':
        leaf = brackets[n].strCluster
        production.append(father + '->' + leaf)
        production2.append(father + '->' + leaf)
        NR_dict[leaf] += 1
        NR_dict2[leaf] += 1
    else:
        leaves = []
        numa = numb = 0
        for m in range(n + 1, len(brackets), 1):
            if brackets[m].numStart > numb:
                numa = brackets[m].numStart
                numb = brackets[m].numEnd
                if numa > numA and numb < numB:
                    son = brackets[m].strPos
                    leaves.append(son)
                    N_dict[son] += 1
                    N_dict2[son] += 1
                else:
                    production.append(father + '->' + ' '.join(leaves))
                    NR_dict[' '.join(leaves)] += 1
                    if len(leaves) > 2:
                        while len(leaves) > 2:
                            one = leaves[-2]
                            two = leaves[-1]
                            leaves.pop()
                            leaves.pop()
                            production2.append('@' + father + '->' + one + ' ' + two)
                            N_dict2['@' + father] += 1
                            NR_dict2[one + ' ' + two] += 1
                            leaves.append('@' + father)
                        production2.append(father + '->' + leaves[0] + ' ' + leaves[1])
                        NR_dict2[leaves[0] + ' ' + leaves[1]] += 1
                    else:
                        production2.append(father+'->'+' '.join(leaves))
                        NR_dict2[' '.join(leaves)] += 1
                    break

# 未二叉化的产生式
with open('prodution.txt', 'w', encoding='utf-8') as fw:
    for i in production:
        arr = i.strip().split('->')
        fw.write(i + '\t\t' + '%.8f' % (NR_dict[arr[1]] / N_dict[arr[0]]) + '\n')

# 二叉化的产生式
with open('prodution2.txt', 'w', encoding='utf-8') as fw:
    for i in production2:
        arr = i.strip().split('->')
        fw.write(i + '\t\t' + '%.8f' % (NR_dict2[arr[1]] / N_dict2[arr[0]]) + '\n')
