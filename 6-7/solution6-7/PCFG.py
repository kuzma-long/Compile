# !/usr/bin/env python3
# -*- coding: utf-8 -*-


from collections import defaultdict


class PCFG(object):

    # N_dict - count nonterminal
    # NR_dict - count relation X->Y1 Y2 (X Y1 Y2 are nonterminal)
    # TR_dict - count relation X->y (X is nonterminal y is terminal)
    def __init__(self):
        self.N_dict = defaultdict(int)
        self.NR_dict = defaultdict(int)
        self.TR_dict = defaultdict(int)
        self.freq=defaultdict(int)

    def fit(self, train_corpus):
        with open(train_corpus, 'r',encoding='utf-8') as f:
            for line in f:
                arr = line.strip().split('->')
                self.N_dict[arr[0]] += 1;
                if len(arr[1].split())!=1:
                    arr2 = arr[1].split()
                    if len(arr2) > 2:
                        self.N_dict[arr2[0]] += 1
                        self.N_dict[arr2[1]] += 1
                        self.NR_dict[(arr[0], arr2[0], arr2[1])] += 1
                        self.freq[(arr[0], arr2[0], arr2[1])]=float(arr2[2])
                    else:
                        if arr2[0].islower():
                            self.TR_dict[(arr[0], arr2[0])] += 1
                            self.freq[(arr[0], arr2[0])] = float(arr2[1])
                        else:
                            self.N_dict[arr2[0]]+=1
                            self.NR_dict[(arr[0],arr2[0])]+=1
                            self.freq[(arr[0],arr2[0])]=float(arr2[1])


    # Return parse tree
    def parse(self, sentence):
        import json
        print(json.dumps(self.CKY(sentence.split())))

    # CKY algorithm
    # 适用于CNF (Chomsky normal form)
    def CKY(self, sentence):
        n = len(sentence)
        pi = defaultdict(float)
        bp = {}  # backpointer
        N = self.N_dict.keys()

        for i in range(n):
            word = sentence[i]
            for X in N:
                pi[(i, i, X)] = self.freq[(X, word)]
                bp[(i, i, X)] = 'shit'

        for i in range(n):
            for j in range(n):
                k = i + j
                if k >= n: continue
                for X in N:
                    max_score = 0
                    argmax = None
                    for R in self.NR_dict.keys():
                        if R[0] == X and len(R)==3:  # start from X
                            Y, Z = R[1:]
                            for s in range(j, k):
                                if pi[(j, s, Y)] and pi[(s + 1, k, Z)]:
                                    score = self.freq[(X, Y, Z)] * pi[(j, s, Y)] * pi[s + 1, k, Z]
                                    if max_score < score:
                                        max_score = score
                                        argmax = Y, Z, s
                    if max_score:
                        pi[j, k, X] = max_score
                        bp[j, k, X] = argmax
                que=[]
                for fuck in bp:
                    if fuck[0]==j and fuck[1]==k and bp[fuck]!=None:
                        Y2=fuck[2]
                        que.append(Y2)
                while len(que)>0:
                    X2=que[0]
                    que=que[1:]
                    for R2 in self.NR_dict:
                        if len(R2)==2 and R2[1]==X2:
                            Z2=R2[0]
                            if self.freq[(Z2,X2)]*pi[(j,k,X2)]>pi[(j,k,Z2)]:
                                pi[(j,k,Z2)]=self.freq[(Z2,X2)]*pi[(j,k,X2)]
                                bp[(j,k,Z2)]=X2,'',k
                                if X2 not in que:
                                    que.append(X2)




        # return
        if pi[(0, n - 1, 'S')]:
            return self.recover(sentence, bp, 0, n - 1, 'S')
        else:
            print("error")

    #  Return the list of the parsed tree with back pointers.
    def recover(self, sentence, bp, i, j, X):
        if i == j:
            if bp[i,j,X]!='shit':
                Y,Z,s=bp[(i,j,X)]
                return [X,self.recover(sentence,bp,i,j,Y)]
            else:
                return [X, sentence[i]]
        else:
            Y, Z, s = bp[i, j, X]
            if Z=='':
                return [X,self.recover(sentence,bp,i,s,Y)]
            else:
                return [X, self.recover(sentence, bp, i, s, Y), self.recover(sentence, bp, s + 1, j, Z)]

parser = PCFG()
parser.fit('toy.txt')
parser.parse('fish people fish tanks')

'''
print(parser.N_dict)
print(parser.NR_dict)
print(parser.TR_dict)
'''