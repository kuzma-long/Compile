TransProbMatrix = {'B': {'B': 0, 'E': 0, 'M': 0, 'S': 0}, 'E': {'B': 0, 'E': 0, 'M': 0, 'S': 0},
                   'M': {'B': 0, 'E': 0, 'M': 0, 'S': 0}, 'S': {'B': 0, 'E': 0, 'M': 0, 'S': 0}}
EmitProbMatrix = {'B': {}, 'E': {}, 'M': {}, 'S': {}}
InitStatus = {'B': 0, 'E': 0, 'M': 0, 'S': 0}
states = ['B', 'E', 'M', 'S']


def readFile(path):
    try:
        with open(path, 'r') as rf:
            lines = rf.readlines()  # 按行读取
    except FileNotFoundError as e:  # 找不到文件的异常处理
        print("File Not Found!")
    return lines


'''
此函数用于将文件读出并按空白符进行分割
input:输入文件路径file
return:一个字符串列表，列表里的每一个元素为按空白符分割后的词
'''


def readDict(file):
    try:
        with open(file, "r") as rd:
            answer = rd.read().split()  # 按空白符进行分割
    except FileNotFoundError as e:  # 找不到文件的异常处理
        print("File Not Found!")
    return answer


def upDate(path):
    lines = readFile(path)
    for line in lines:
        words = line.strip().split()
        if len(words) > 0:
            if len(words[0]) == 1:
                InitStatus['S'] += 1
            else:
                InitStatus['B'] += 1
        for i in range(len(words)):
            this = words[i]
            if len(this) == 1:
                temp = EmitProbMatrix['S'].get(this, 0)
                EmitProbMatrix['S'][this] = temp + 1
                if i < len(words) - 1:
                    next = words[i + 1]
                    if len(next) == 1:
                        TransProbMatrix['S']['S'] += 1
                    else:
                        TransProbMatrix['S']['B'] += 1
            elif len(this) == 2:
                temp1 = EmitProbMatrix['B'].get(this[0], 0)
                EmitProbMatrix['B'][this[0]] = temp1 + 1
                temp2 = EmitProbMatrix['E'].get(this[1], 0)
                EmitProbMatrix['E'][this[1]] = temp2 + 1
                TransProbMatrix['B']['E'] += 1
                if i < len(words) - 1:
                    next = words[i + 1]
                    if len(next) == 1:
                        TransProbMatrix['E']['S'] += 1
                    else:
                        TransProbMatrix['E']['B'] += 1
            elif len(this) > 2:
                length = len(this)
                temp3 = EmitProbMatrix['B'].get(this[0], 0)
                EmitProbMatrix['B'][this[0]] = temp3 + 1
                temp4 = EmitProbMatrix['E'].get(this[length - 1], 0)
                EmitProbMatrix['E'][this[length - 1]] = temp4 + 1
                for j in range(1, length - 1):
                    temp5 = EmitProbMatrix['M'].get(this[j], 0)
                    EmitProbMatrix['M'][this[j]] = temp5 + 1
                    TransProbMatrix['M']['M'] += 1
                TransProbMatrix['M']['M'] -= 1
                TransProbMatrix['B']['M'] += 1
                TransProbMatrix['M']['E'] += 1
                if i < len(words) - 1:
                    next = words[i + 1]
                    if len(next) == 1:
                        TransProbMatrix['E']['S'] += 1
                    else:
                        TransProbMatrix['E']['B'] += 1

    for i in TransProbMatrix:
        sum = 0
        for j in TransProbMatrix[i]:
            sum += TransProbMatrix[i][j]
        for k in TransProbMatrix[i]:
            TransProbMatrix[i][k] /= sum

    for i in EmitProbMatrix:
        sum = 0
        for j in EmitProbMatrix[i]:
            sum += EmitProbMatrix[i][j]
        for k in EmitProbMatrix[i]:
            EmitProbMatrix[i][k] /= sum

    all = 0
    for i in InitStatus:
        all += InitStatus[i]
    for j in InitStatus:
        InitStatus[j] /= all


def viterbi(path):
    lines = readFile(path)
    fw = open('HMM_pku_out.txt', 'w')
    for line in lines:
        line = line.strip()
        if line != '':
            length = len(line)
            weight = [[0 for i in range(length)] for j in range(4)]
            path = [[-1 for i in range(length)] for j in range(4)]
            weight[0][0] = InitStatus['B'] * EmitProbMatrix['B'].get(line[0], 0)
            weight[1][0] = 0
            weight[2][0] = 0
            weight[3][0] = InitStatus['S'] * EmitProbMatrix['S'].get(line[0], 0)
            kuzma=0
            for i in range(4):
                if weight[i][0]==0:
                    kuzma+=1
            if kuzma==4:
                for j in range(4):
                    weight[j][0]=0.0000000000000000000001   #平滑处理
            for i in range(1, length):
                num=0
                for j in range(len(states)):
                    if line[i] not in EmitProbMatrix[states[j]]:
                        num+=1
                if num==4:
                    for m in range(len(states)):
                        EmitProbMatrix[states[m]][line[i]]=0.0000000000000000000001     #平滑处理
                for j in range(len(states)):
                    for k in range(len(states)):
                        temp = weight[k][i - 1] * TransProbMatrix[states[k]][states[j]] * EmitProbMatrix[states[j]].get(
                            line[i], 0)
                        if temp > weight[j][i]:
                            weight[j][i] = temp
                            path[j][i] = k
            road = []
            last = length - 1
            if weight[1][last] > weight[3][last]:
                road.append(1)
                k = path[1][last]
            elif weight[1][last]<weight[3][last]:
                road.append(3)
                k = path[3][last]
            else:
                road.append(-1)
                k=-1
            last -= 1
            road.append(k)
            while last > 0:
                t = path[k][last]
                road.append(t)
                k = t
                last -= 1
            road.reverse()
            # print(road)
            w = ''
            for i in range(length):
                if road[i] == 3:
                    w = line[i]
                    fw.write(w + ' ')
                    w = ''
                elif road[i] == 1:
                    w += line[i]
                    fw.write(w + ' ')
                    w = ''
                else:
                    w += line[i]
            fw.write(w+'\n')


'''
此函数用于检查输出文件out和答案的匹配度，输出相关的值
input:out,answer
output:P/R/F
'''


def check(out, answer):
    right = 0  # 记录匹配正确的词的个数
    out_index = 0  # 输出文件的下标
    answer_index = 0  # 答案的下标
    i = 0
    while out_index < len(out):  # 遍历输出文件
        temp_out = out[out_index]
        temp_answer = answer[answer_index]
        if temp_out == temp_answer:  # 匹配成功的情况
            right += 1
        else:
            # 匹配不成功时，让两个下标轮流前进，并将新词连接到原来的词上，# 使输出文件当前的词与答案当前的词长度相等
            if len(temp_out) < len(temp_answer):
                while len(temp_out) < len(temp_answer):
                    out_index += 1
                    temp_out += out[out_index]
                    while len(temp_out) > len(temp_answer):
                        answer_index += 1
                        temp_answer += answer[answer_index]
            else:
                while len(temp_out) > len(temp_answer):
                    answer_index += 1
                    temp_answer += answer[answer_index]
                    while len(temp_out) < len(temp_answer):
                        out_index += 1
                        temp_out += out[out_index]
        # 让两个下标分别前进一位，使当前下标位置一样，重新开始循环
        out_index += 1
        answer_index += 1
    precision = right / len(out)  # 计算正确率
    recall = right / len(answer)  # 计算召回率
    print("正确率（Precision）=" + str(right) + '/' + str(len(out)) + '=' + '{:.2%}'.format(precision))
    print("召回率（Recall）=" + str(right) + '/' + str(len(answer)) + '=' + '{:.2%}'.format(recall))
    print("F值=(" + str(right) + '/' + str(len(out)) + ')*(' + str(right) + '/' + str(len(answer)) + ")*2/(" + str(
        right) + '/' + str(len(out)) + '+' + str(right) + '/' + str(len(answer)) + ")=" + '{:.2%}'.format(
        precision * recall * 2 / (precision + recall)))


training = 'pku_training.txt'
test = 'pku_test.txt'
out = 'HMM_pku_out.txt'
answer = 'pku_test_gold.txt'

upDate(training)
# print(TransProbMatrix)
# print(EmitProbMatrix)
# print(InitStatus)
viterbi(test)
check(readDict(out), readDict(answer))
