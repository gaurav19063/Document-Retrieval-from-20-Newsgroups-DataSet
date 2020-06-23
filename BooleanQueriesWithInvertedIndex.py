from nltk.tokenize import word_tokenize
import  os
def fixit(dict1):
    dict2 = {}

    for x in dict1.keys():
        dict2[x]=sorted(dict1[x][1:])
        dict2[x].insert(0,dict1[x][0])
    return dict2
def loadData():
    path="/home/gaurav/Desktop/IIITD/IR/Assignments/assignment1/20_newsgroups"
    i=0
    dict1={}
    all_doc = []
    for x in os.listdir(path):

        for y in os.listdir(path+"/"+x):
            all_doc.append(int(y))
            path2=path+"/"+x+"/"+y
            f = open(path2,encoding='windows-1252')
            i=i+1
            print(i)
            terms=word_tokenize(f.read())
            terms=set(terms)
            for w in terms:
                if w in dict1.keys():
                    dict1[w][0]=dict1[w][0]+1
                    dict1[w].append(int(y))

                else:
                    dict1[w]=[1]
                    dict1[w].append(int(y))



    dict1=fixit(dict1)
    return dict1,sorted(all_doc)



def Query_NOT(x,dict1,all_doc):
    count=0
    list1=[]
    if(dict1[x][0]==0):
        return all_doc
    for a in all_doc:
        flag = 0
        for b in (dict1[x])[1:]:
            if(a==b):
                flag=1

                break
            count = count + 1
        if(flag==1):
            continue
        else:
            list1.append(a)
        # count = count + 1
    list1.insert(0,len(list1))
    return list1,count

def findMin(lists):
    # print(len(lists))
    if(len(lists)<=2):
        return 0, 1


    j=0;
    min1=20001
    min2=20001
    min1_ind=-1
    min2_ind=-1
    j=0
    # print(lists)
    for i in lists:
        # print(i[0],min2)
        if(i[0]<min1):
            min1=min2
            min1_ind=min2_ind
            min2=i[0]
            min2_ind=j
        j=j+1
        # print(min1, min2)


    # print (min1_ind,min2_ind)
    return min1_ind,min2_ind
def intersection(list1,list2):
    i = 0
    j = 0
    list4 = []
    # print(list1)
    # print(list2)
    count = 0
    while i < len(list1) and j < len(list2):

        if (list1[i] == list2[j]):
            # print(list1[i], list2[j])
            list4.append(list1[i])
            i = i + 1
            j = j + 1
        elif list1[i] > list2[j]:
            # print(i,j)
            j = j + 1
        else:
            i = i + 1
        count = count + 1
    return list4,count

def intersection_st(lists,min1,min2):
    list1=lists[min1][1:].copy()
    # print(list1)
    list2=lists[min2][1:].copy()

    list4,count=intersection(list1, list2)
    list4.insert(0,len(list4))
    lists.remove(lists[min1])
    lists.remove(lists[min2-1])
    lists.insert(min1,list4)
    # print(list4)
    return lists,count


def optimizedQuery_AND(lists,counts):

    if(len(lists)==1):
        return lists,counts

    min1,min2=findMin(lists)

    lists,count=intersection_st(lists,min1,min2)
    # print(lists)
    counts=counts+count
    return optimizedQuery_AND(lists,counts)



def UNION(list1,list2):
    i=0
    j=0
    count=0
    list3=[]
    while i<len(list1) and j<len(list2):
        if(list1[i]==list2[j]):
            list3.append(list2[j])
            i=i+1
            j=j+1
        elif(list1[i]>list2[j]):
            list3.append(list2[j])
            j=j+1
        else:
            list3.append(list1[i])
            i=i+1
        count=count+1
    while i < len(list1):
        list3.append(list1[i])
        i = i + 1
    while j < len(list2):
        list3.append(list2[j])
        j = j + 1
    list3.insert(0,len(list3))
    return list3,count


def fun1(list):

    list1 = []
    list2 = []
    list4=[]
    j = 0
    count=0
    for i in list:
        if (i != 'AND' and i != 'OR'):
            list2.append(j)
        else:
            list2.append(list[j])
        j = j + 1
    # print(list2)
    k = 0
    list2.append('OR')
    for i in range(len(list2) - 1):
        # list2 = []
        i = i + 1
        # print(i)
        if (list2[i] == 'AND'):
            list1.append(list2[i - 1])
            list1.append(list2[i + 1])
            k = k + 1
            j = j + 1

        elif ((list2[i] == 'OR' and j > 0) or (i == len(list2) - 1 and list2[i] == 'AND')) and k > 0:
            j = 0
            lst=set(list1)
            # print(lst)



            Klist = []

            list4.append(lst)
            for r in  lst:

                Klist.append(list[r])
            list1 = []

            ttlist,count1=optimizedQuery_AND(Klist, count)
            # print("yes4")
            count=count+count1


            c=0
            list5=list.copy()

            for r in lst:
                # print(r)
                if(c==0):
                    list[r]=ttlist[0]


                    continue

    # list.remove(list[-1])
    print("--------------")

    # print("--------------")
    lis=list.copy()
    # for i in lis:
    #     print(i)


    list6=[]
    i=0
    p=0
    for k in lis:

        if(k=="AND" and p==0):
            list6.append(lis[i-1])
            p=p+1
        elif(k=="OR") :
            if(p==0):
                list6.append(lis[i-1])

            list6.append(lis[i] )
            p=0


        i=i+1
    if(lis[i-2]!="AND"):
        list6.append(lis[i-1])

    i=0
    for k in list6:
        # print(k)
        if(k=="OR"):
           # print(list6[i-1][1:], list6[i+1][1:])
           lt,count4= UNION(list6[i-1][1:], list6[i+1][1:])
           # print(lt)
           list6[i+1]=lt
           count=count+count4
           # print(lt)

        i=i+1


    # print(list6[-1])





    return list6[-1],count





def hetroQuery(q_words,list1):
    # for i in list1:
    #     print(i)





    AND_ind= [i for i, x in enumerate(q_words) if x == "AND"]
    count1=0
    list2=[]
    i=0
    pre=0
    j=0
    k=0
    for i in q_words:
        if(i!="AND" and i!="OR"):
            q_words[j]=list1[k]
            k=k+1
        j=j+1
    # for i in q_words:
    #     print(i)


    q_words,count2=fun1(q_words)
    count1=count1+count2
    # j=0
    #
    # for i in q_words:
    #     if(i=="OR"):
    #         list3,count=UNION(q_words[j-1][1:],q_words[j+1][1:])
    #         print("yes")
    #         print(list3)
    #         print(count)
    #     j=j+1





    for i in range (len(AND_ind)-1):
        list3=[]
        if(AND_ind[i]==AND_ind[i+1]-2):
            list3.append(i)






    return q_words ,count1

def run_query(query,dict1,all_doc):
    q_words = word_tokenize(query)

    lists1=[]
    i=0
    count=0
    p_words=q_words.copy()


    for x in p_words:
        # print(x)
        if(i%2==1 and x!="NOT"):
            if x in dict1.keys():
                l,count1=Query_NOT(x,dict1,all_doc)

                print(count1)
                lists1.append(l)
                count=count+count1
                # print("yes")


            else:
                lists1.append([0])

            i=0



        elif x=="NOT":
            i=i+1
            q_words.remove(x)




        elif x!="AND" and x!="OR" and x!="NOT":
            # print(dict1[x])
            # lists1.append()
            if x in dict1.keys():
                lists1.append(dict1[x])
            else:
                lists1.append([0])


    count_list=[]
    # count_list.append(q_words.count("NOT"))
    count_list.append(q_words.count("AND"))
    count_list.append(q_words.count("OR"))
    # print(count_list)
    if count_list[0]>=1 and count_list[1]==0:

       lists1,counts= optimizedQuery_AND(lists1,count)
       print("DOCS: ",lists1)
       # print(len(lists1))
       count=count+counts
       print("Count :",count)

    else:
        # print(q_words)
        # print(lists1)
        lists1,count3=hetroQuery(q_words, lists1)
        # print(docs)
        count = count + count3
        # print(count)
        print("DOCS: ",lists1)
        print("Count :",count)
        # return


    # ------------------------------------------------------------------------------------------
dict1,all_doc=loadData()
# print(len(all_doc))
# dict1={}
# all_doc=[]

query="input()"
while(query!="-1"):
    query = input()
    run_query(query,dict1,all_doc)
# print(lists)
# print(lists)


