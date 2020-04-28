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


'''
此函数用于对文件进行按行读取
input:输入文件路径file
return:一个字符串列表，列表里的每一个元素是输入文件的每一行
'''
def readFile(file):
    try:
        with open(file, 'r') as rf:
            lines = rf.readlines()  # 按行读取
    except FileNotFoundError as e:  # 找不到文件的异常处理
        print("File Not Found!")
    return lines


'''
此函数对file和dict进行匹配，对file文件进行分词分割，并将分割后的文件输出到path路径
input:一个字符串列表file，其中的元素为需要进行分割的文件的每一行
      一个字符串列表dict，其中的元素为进行匹配的字典的每一个词
      将匹配完的结果输出的路径path
'''
def corpusMatch(file, dict, path):
    result = []  # 存储最后的结果
    for line in file:  # 遍历文件的每一行
        line_length = len(line)  # 存储当前处理的这一行的长度
        while line_length > 0:
            max_length = 7  # 词的最大匹配长度
            while max_length > 0:
                temp = line[0:max_length]  # 截取出当前所能截取的最长的词
                if temp == '\n':  # 单独处理行尾的换行符
                    result.append('\n')
                    line_length = 0
                    break
                if temp in dict:  # 如果当前截取出的词能够匹配
                    result.append(temp)
                    line = line[max_length:]  # 用切片将匹配出来的词切除
                    line_length = len(line)
                    break
                else:  # 如果当前截取出的词未能匹配
                    if max_length == 1:  # 当前的词为单字
                        result.append(temp)
                        line = line[max_length:]
                        line_length = len(line)
                        break
                    else:  # 当前的词不是单字，将最大匹配长度减1
                        max_length = max_length - 1
    with open(path, "w") as wf:  # 将结果输出到指定路径
        for word in result:
            if word == '\n':
                wf.write(word)
            else:
                wf.write(word + ' ')


'''
此函数用于检查输出文件out和答案的匹配度，输出相关的值
input:out,answer
output:P/R/F
'''
def check(out, answer):
    right = 0  # 记录匹配正确的词的个数
    out_index = 0  # 输出文件的下标
    answer_index = 0  # 答案的下标
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


# 用到的路径
test_path = "pku_test.txt"  # 输入文件路径
dict_path = "pku_training_words.txt"  # 词典路径
answer_path = "pku_test_gold.txt"  # 答案路径
out_path = "FMM_pku_out.txt"  # 输出文件路径

# 主要操作
file = readFile(test_path)  # 读入需要操作的文件
temp=readDict(dict_path)
corpus_dict={}
for i in temp:
    corpus_dict[i]=1
corpusMatch(file, corpus_dict, out_path)  # 将文件与词典进行最大匹配
check(readDict(out_path), readDict(answer_path))  # 检查输出文件与答案的匹配程度
