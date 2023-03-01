import pandas as pd
def obj_1(items,data):
    change_num=0
    T=0
    for item in items:
        t=data[data['id']==item].model.values[0]
        if t !=T:
            change_num+=1
            T=t
    return change_num

def obj_try1(items,c_index,data):
    c1 = items[:c_index[0][0] - 1]
    c2 = items[c_index[0][0] - 1:c_index[1][0]]
    c2.reverse()
    c3 = items[c_index[1][0]:]
    items_ = c1 + c2 + c3
    new_data = pd.DataFrame(columns=data.columns.values)
    for i in range(len(items_)):
        new_data.loc[i, :] = data[data['id'] == items_[i]].values[0]
    return items_

def obj_1_new(items,data,Fun):
    change_index=[]
    T=-1
    change_count=0
    for i in range(len(items)):
        t=data.loc[i].model
        change_count+=1
        if (t !=T) :
            change_index.append([i,change_count,T])
            T = t
            change_count = 0
    change_index=change_index[1:]
    c_index=[]
    for i in range(len(change_index)):
        if change_index[i][1]<15:
            c_index.append(change_index[i])
    Num=0
    TT=1
    Function=Fun[3]
    while TT:
        if len(c_index)==0:
            items_=items
            TT=0
        elif (len(c_index)==1):
            c = c_index[0]
            #下移
            for i in range(c[0],c[0]+10):
                if (data.loc[i].color_same == 0) & (data.loc[i].color_body == data.loc[i-c[1]].color_body):
                    #拼接序列
                    t0=data.loc[:i-c[1]-1]
                    t1=data.loc[i-c[1]+1:i]
                    t2=data.loc[i-c[1]:i-c[1]]
                    t3=data.loc[i+1:]
                    data=pd.concat([t0,t1,t2,t3],ignore_index=True)
                    c[0]+=1
                else:
                    break
            items_=data['id'].tolist()
            if c[2]==0:   #从前往后
                for i in range(len(items_)):
                    if (data.loc[i].derailleur == 0) & (data.loc[i].color_roof == 10) & (data.loc[i].color_body!=data.loc[min([i+1,len(items_)-1])].color_roof) & (i > 23):
                        km = c[0]+Num-c[1]+1
                        Num = i
                        t0=items_[i+1:km]
                        t1=items_[:i+1]
                        t2=items_[km:]
                        items_ = t0+t1+ t2
                        new_data = pd.DataFrame(columns=data.columns.values)
                        for i in range(len(items_)):
                            new_data.loc[i, :] = data[data['id'] == items_[i]].values[0]
                        # km = len(t0)
                        # for i in range(len(items_) - 1, c_index[1][0], -1):
                        #     if (new_data.loc[i].derailleur == 0) & (new_data.loc[i].color_roof == 10) & (
                        #             new_data.loc[i - 1].derailleur == 0) & (new_data.loc[i - 1].color_roof == 10):
                        #         items_ = items_[:km] + [items_[i - 1]] + items_[km:i - 1] + items_[i:]
                        #         break
                        # new_data = pd.DataFrame(columns=data.columns.values)
                        # for i in range(len(items_)):
                        #     new_data.loc[i, :] = data[data['id'] == items_[i]].values[0]
                        # print()
                        break
            else:   #从后往前
                for i in range(len(items_)-1,-1,-1):
                    if (data.loc[i].derailleur==0) & (data.loc[i].color_roof==10) & (data.loc[i].color_body!=data.loc[min([i+1,len(items_)-1])].color_roof) & (len(items_)-i>23):
                        km = c[0]+ Num
                        Num=len(items_)-i
                        items_=items_[:km]+items_[i:]+items_[km:i]
                        new_data = pd.DataFrame(columns=data.columns.values)
                        for i in range(len(items_)):
                            new_data.loc[i, :] = data[data['id'] == items_[i]].values[0]
                        #在末尾添加一个10
                        km=c[0]+Num
                        for i in range(len(items_)-1,-1,-1):
                            if (new_data.loc[i].derailleur == 0) & (new_data.loc[i].color_roof == 10) & (new_data.loc[i-1].derailleur == 0) & (new_data.loc[i-1].color_roof == 10):
                                items_ = items_[:km] + [items_[i-1]] + items_[km:i-1]+items_[i:]
                                break
                        new_data = pd.DataFrame(columns=data.columns.values)
                        for i in range(len(items_)):
                            new_data.loc[i, :] = data[data['id'] == items_[i]].values[0]
                        # data=new_data
                        break
            obj_new = obj_4(items_, new_data, Fun[1])
            if obj_new < Fun[3]:
                TT = 0
                Function=obj_new
            else:
                TT = 0
                items_=items
                print('还需进一步优化:序列变长')
        elif (len(c_index) == 2) & (sum(data.loc[c_index[0][0] - 1:c_index[1][0]-1].color_same.values.tolist())==0):
                items_=obj_try1(items, c_index,data)   #先倒序试试
                new_data = pd.DataFrame(columns=data.columns.values)
                for i in range(len(items_)):
                    new_data.loc[i, :] = data[data['id'] == items_[i]].values[0]
                obj_new=obj_4(items_, new_data, Fun[1])
                if obj_new<Fun[3]:
                    TT=0
                    Function = obj_new
                else:
                    TT = 0
                    items_ = items
                    print('还需进一步优化:序列变长')
        elif (len(c_index)==2) & (c_index[0][0]>23) & (c_index[1][0]<(len(items)-23)) & (c_index[0][2]==1) & (c_index[1][2]==0):
            items_=items
            for c in c_index:
                if c[2]==0:   #从前往后
                    for i in range(len(items_)):
                        if (data.loc[i].derailleur == 0) & (data.loc[i].color_roof == 10) & (data.loc[i].color_body!=data.loc[min([i+1,len(items_)-1])].color_roof) & (i > 23):
                            km = c[0]+Num-c[1]+1
                            Num = i
                            t0=items_[i+1:km]
                            t1=items_[:i+1]
                            t2=items_[km:]
                            items_ = t0+t1+ t2
                            new_data = pd.DataFrame(columns=data.columns.values)
                            for i in range(len(items_)):
                                new_data.loc[i, :] = data[data['id'] == items_[i]].values[0]
                            # km = len(t0)
                            # for i in range(len(items_) - 1, c_index[1][0], -1):
                            #     if (new_data.loc[i].derailleur == 0) & (new_data.loc[i].color_roof == 10) & (
                            #             new_data.loc[i - 1].derailleur == 0) & (new_data.loc[i - 1].color_roof == 10):
                            #         items_ = items_[:km] + [items_[i - 1]] + items_[km:i - 1] + items_[i:]
                            #         break
                            # new_data = pd.DataFrame(columns=data.columns.values)
                            # for i in range(len(items_)):
                            #     new_data.loc[i, :] = data[data['id'] == items_[i]].values[0]
                            # print()
                            break
                else:   #从后往前
                    for i in range(len(items_)-1,c_index[1][0],-1):
                        if (data.loc[i].derailleur==0) & (data.loc[i].color_roof==10) & (data.loc[i].color_body!=data.loc[min([i+1,len(items_)-1])].color_roof) & (len(items_)-i>23):
                            km = c[0]+ Num
                            Num=len(items_)-i
                            items_=items_[:km]+items_[i:]+items_[km:i]
                            new_data = pd.DataFrame(columns=data.columns.values)
                            for i in range(len(items_)):
                                new_data.loc[i, :] = data[data['id'] == items_[i]].values[0]
                            #在末尾添加一个10
                            km=c[0]+Num
                            for i in range(len(items_)-1,c_index[1][0],-1):
                                if (new_data.loc[i].derailleur == 0) & (new_data.loc[i].color_roof == 10) & (new_data.loc[i-1].derailleur == 0) & (new_data.loc[i-1].color_roof == 10):
                                    items_ = items_[:km] + [items_[i-1]] + items_[km:i-1]+items_[i:]
                                    break
                            new_data = pd.DataFrame(columns=data.columns.values)
                            for i in range(len(items_)):
                                new_data.loc[i, :] = data[data['id'] == items_[i]].values[0]
                            # data=new_data
                            break
            obj_new = obj_4(items_, data, Fun[1])
            if obj_new < Fun[3]:
                TT = 0
                Function = obj_new
            else:
                TT = 0
                items_=items
                print('还需进一步优化:序列变长')
        elif (len(c_index)==2):
            items_=items
            c=c_index[0]
            if c_index[0][2]==1:  #从前往后
                for i in range(len(items_)):
                    if (data.loc[i].derailleur == 0) & (data.loc[i].color_roof == 10) & (data.loc[i].color_body!=data.loc[min([i+1,len(items_)-1])].color_roof) & (i > 23):
                        km = c[0]+Num-c[1]+1
                        Num = i
                        t0=items_[i+1:km]
                        t1=items_[:i+1]
                        t2=items_[km:]
                        items_ = t0+t1+ t2
                        new_data = pd.DataFrame(columns=data.columns.values)
                        for i in range(len(items_)):
                            new_data.loc[i, :] = data[data['id'] == items_[i]].values[0]
                        # km = len(t0)
                        # for i in range(len(items_) - 1, c_index[1][0], -1):
                        #     if (new_data.loc[i].derailleur == 0) & (new_data.loc[i].color_roof == 10) & (
                        #             new_data.loc[i - 1].derailleur == 0) & (new_data.loc[i - 1].color_roof == 10):
                        #         items_ = items_[:km] + [items_[i - 1]] + items_[km:i - 1] + items_[i:]
                        #         break
                        # new_data = pd.DataFrame(columns=data.columns.values)
                        # for i in range(len(items_)):
                        #     new_data.loc[i, :] = data[data['id'] == items_[i]].values[0]
                        # print()
                        break
            else:   #从后往前
                for i in range(len(items_)-1,c_index[1][0],-1):
                    if (data.loc[i].derailleur==0) & (data.loc[i].color_roof==10) & (data.loc[i].color_body!=data.loc[min([i+1,len(items_)-1])].color_roof) & (len(items_)-i>23):
                        km = c[0]+ Num
                        Num=len(items_)-i
                        items_=items_[:km]+items_[i:]+items_[km:i]
                        new_data = pd.DataFrame(columns=data.columns.values)
                        for i in range(len(items_)):
                            new_data.loc[i, :] = data[data['id'] == items_[i]].values[0]
                        #在末尾添加一个10
                        km=c[0]+Num
                        for i in range(len(items_)-1,c_index[1][0],-1):
                            if (new_data.loc[i].derailleur == 0) & (new_data.loc[i].color_roof == 10) & (new_data.loc[i-1].derailleur == 0) & (new_data.loc[i-1].color_roof == 10):
                                items_ = items_[:km] + [items_[i-1]] + items_[km:i-1]+items_[i:]
                                break
                        new_data = pd.DataFrame(columns=data.columns.values)
                        for i in range(len(items_)):
                            new_data.loc[i, :] = data[data['id'] == items_[i]].values[0]
                        # data=new_data
                        break
                if c[2] == 0:  # 从前往后
                    for i in range(len(items_)):
                        if (data.loc[i].derailleur == 0) & (data.loc[i].color_roof == 10) & (
                                data.loc[i].color_body != data.loc[min([i + 1, len(items_) - 1])].color_roof) & (
                                i > 23):
                            km = c[0] + Num - c[1] + 1
                            Num = i
                            t0 = items_[i + 1:km]
                            t1 = items_[:i + 1]
                            t2 = items_[km:]
                            items_ = t0 + t1 + t2
                            new_data = pd.DataFrame(columns=data.columns.values)
                            for i in range(len(items_)):
                                new_data.loc[i, :] = data[data['id'] == items_[i]].values[0]
                            break
            obj_new = obj_4(items_, data, Fun[1])
            if obj_new < Fun[3]:
                TT = 0
                Function = obj_new
            else:
                TT = 0
                items_=items
                print('还需进一步优化:序列变长')
        else:
            TT = 0
            items_=items
            print('还需进一步优化')
    Fun=(Fun[0],Fun[1],Fun[2],Function)
    return items_,Fun

def obj_2(items,data):
    T = 0
    count = 0
    index = {}
    new_data = pd.DataFrame(columns=data.columns.values)
    for i in range(len(items)):
        new_data.loc[i, :] = data[data['id'] == items[i]].values[0]
    for i in range(len(items)):
        item = items[i]
        p_color = data[data['id'] == item].color_same.values[0]
        if p_color==0:
            T+=1
        else:
            count += T*T
            T=0
        if T==5:
            count += T * T
            T=0
    return -1*count,index

def obj_2_old(items,data):
    T = 0
    count = -1
    end_color = -1
    index = {}
    last_color = 0
    new_data = pd.DataFrame(columns=data.columns.values)
    for i in range(len(items)):
        new_data.loc[i, :] = data[data['id'] == items[i]].values[0]
    for i in range(len(items)):
        item = items[i]
        t1 = data[data['id'] == item].color_roof.values[0]
        t2 = data[data['id'] == item].color_body.values[0]
        p_color = data[data['id'] == item].color_same.values[0]
        if (t1 == end_color):
            if (T == 5):
                count += 1
                T=1
        else:
            count += 1
            end_color = t1
            # 找分界点
            if ((T == 1) & (last_color == 0)) | (T == 2) | (T == 3) | (T == 4):
                it = data[data['id'] == items[i - 1]]
                # 位置：颜色，个数，模式，是否可以移动
                if i - T -1>-1:
                    or_it = data[data['id'] == items[i - T -1]]
                    or_it_1 = data[data['id'] == items[i - T ]]
                    index[i] = (i, it.color_body.values[0], T, it.model.values[0], or_it.color_body.values[0] != or_it_1.color_roof.values[0])
                else:
                    index[i] = (i, it.color_body.values[0], T , it.model.values[0], True)
            T = 0
        if t2 != t1:
            count += 1
            end_color = t2
            T = 0
        else:
            T += 1
        last_color = p_color
    return count,index

def obj_3(items,data):
    change_num=0
    T=0
    for item in items:
        t=data[data['id']==item].derailleur.values[0]
        if t==1:
            T+=1
            if T>3:
                change_num += 1
        if (t==0) & (T==1):
            change_num += 1
            T = 0
        if t==0:
            T=0
    return change_num

def obj_3_new(items,data):
    if obj_3(items,data)>0:
        T=0
        for i in range(len(items)):
            item=items[i]
            t = data[data['id'] == item].derailleur.values[0]
            if t == 1:
                T += 1
                if T > 3:
                    try:
                        for j in range(i+1,len(items)):
                            if (i!=j) & (data.loc[j].model ==data.loc[i].model) & (data.loc[j].derailleur+data.loc[j+1].derailleur == 0) & (data.loc[j].color_roof+data.loc[j+1].color_roof == 20):
                                if i<j:
                                    t0=items[:i]
                                    t1=items[j:j+1]
                                    t2=items[i:j]
                                    t3=items[j+1:]
                                    items=t0+t1+t2+t3
                                    T=0
                                    new_data = pd.DataFrame(columns=data.columns.values)
                                    for i in range(len(items)):
                                        new_data.loc[i, :] = data[data['id'] == items[i]].values[0]
                                    data =new_data
                                    break
                                else:
                                    items=items[:j]+items[i:i+1]+items[j:i]+items[i+1:]
                                    T=0
                                    new_data = pd.DataFrame(columns=data.columns.values)
                                    for i in range(len(items)):
                                        new_data.loc[i, :] = data[data['id'] == items[i]].values[0]
                                    data = new_data
                                    break
                    except:
                        pass
            if (t == 0) & (T == 1):
                if data.loc[i-1].color_roof == 10:
                    try:
                        for j in range(i+1,len(items)):
                            if (i != j) & (data.loc[j].model == data.loc[i].model) & (data.loc[j].derailleur==0) &(data.loc[j + 1].derailleur==1) &(data.loc[j + 2].derailleur == 1) &(data.loc[j + 3].derailleur == 0)  & (
                                    data.loc[j+1].color_roof + data.loc[j + 2].color_roof+data.loc[j + 3].color_roof == 30):
                                    t0 = items[:i-1]
                                    t1 = items[i-1:i]
                                    t2 = items[i:j+1]
                                    t3 = items[j+1:]
                                    items = t0 + t2 + t1 + t3
                                    new_data = pd.DataFrame(columns=data.columns.values)
                                    for i in range(len(items)):
                                        new_data.loc[i, :] = data[data['id'] == items[i]].values[0]
                                    data = new_data
                                    break
                    except:
                        pass
                T = 0
            if t == 0:
                T = 0
    return items

def obj_4(items,data,obj2):
    t2=obj2 * 80 + len(items) * 80
    t3=len(items)*80
    t1=0
    T4 = 0
    Time=0
    new_data = pd.DataFrame(columns=data.columns.values)
    for i in range(len(items)):
        new_data.loc[i, :] = data[data['id'] == items[i]].values[0]
    for item in items:
        t = data[data['id'] == item].model.values[0]
        if (t == T4) :
            t1 +=80
            Time+=80
        elif (t != T4) & (Time<30*60):
            T4=t
            t1+=30 * 60-Time
        else:
            T4=t
            Time=80
    return t1+t2+t3