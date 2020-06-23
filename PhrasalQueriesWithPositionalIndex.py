from nltk.tokenize import word_tokenize
import  os
import re
def fixit(dict1):
    dict2 = {}
    for x in dict1.keys():
        dict2[x]=sorted(dict1[x][1:])
        dict2[x].insert(0,dict1[x][0])
    return dict2
def loadData():
    path="/home/gaurav/Desktop/IIITD/IR/Assignments/assignment1/mod_data"
    i=0
    dict1={}
    for x in os.listdir(path):

        for y in os.listdir(path+"/"+x):
            path2=path+"/"+x+"/"+y
            f = open(path2,encoding='windows-1252')
            i=i+1
            print(i)
            text=f.read()
            term1=word_tokenize(text)
            terms=set(term1)

            for w in terms:
                dict2 = {}
                ind = [i for i, x in enumerate(term1) if x == w]
                dict2[int(y)] = ind
                if w in dict1.keys():


                    dict1[w][0]=dict1[w][0]+1

                    #dict1[w].append(dict2)
                    # dict2[y].append(ind)
                    dict1[w][1][int(y)]=ind

                else:
                    dict1[w]=[1]
                    dict1[w].append(dict2)



    # dict1=fixit(dict1)
    return dict1








def querys(dict1,q_word):
    list=[]
    for x in q_word[0:1]:
        list1 = []
        for x in dict1[x][1:]:
            # print(x)

            for y in x:
                # print(y)
                if (type(y) == int):
                    # print(type(y))
                    list1.append(y)

    list2=[]
    i=1
    for t in q_word[1:]:

        for x in dict1[t][1:]:
            # print(x)

            for y in x:
                flag = 0
                if (type(y) == int):
                    if y in list1:


                        for p in dict1[t][1][y]:
                            for q in dict1[q_word[i-1]][1][y]:
                                if (p-q==1):
                                    list2.append(y)
                                    flag=1
                                    break
                            if(flag):
                                break

        list1=list2.copy()
    i = i + 1
    print("Docs:",list1)














# ------------------------------------------------------------------------------------------
dict1=loadData()
print(dict1)
query=input()
q_word=word_tokenize(query)

querys(dict1,q_word)

