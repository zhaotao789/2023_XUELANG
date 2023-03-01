from seq_mater import *
from obj import *
import random
from collections import Counter
from tqdm import tqdm
import time
class weld:
    def __init__(self,bins,DATA,match_list,TYPE,time_start,Sort_i,Parateo):
        self.DATA = DATA
        self.bins=bins
        self.num=len(bins)
        self.min_num=23
        self.bins.sort(key=lambda x:x.num,reverse=True)
        self.maters=[]
        self.match_list=match_list
        self.TYPE=TYPE
        self.time_start=time_start
        self.Sort_i=Sort_i
        self.Parateo=Parateo

    def _mater_factory(self,min_num):
        return seq_mater(min_num)

    def change_two_1(self,a, b):
        for i in b.order:
            a.insert(i)
            a.num+=1

    def change_(self,a, b,index):
        for i in b.order:
            a.insert(i)
            a.num+=1

    def change_two_2(self,a, b):
        if len(b.order)==1:
            item = b.order[-1]
            a.order.append(item)
            a.num+=1
        else:
            for i in b.order:
                a.order.append( i)
                a.num += 1

    def change_direction(self,md):
        new_md=[]
        for i in range(len(md)-1,-1,-1):
            new_md.append(md[i])
        return new_md

    def insert_two_2(self,mater, mod,mt):
        mater.order=mater.order[:mt+1]+mod+mater.order[mt+1:]
        mater.num+=len(mod)

    def submit(self,maters,model_0,model_1,model_05):
        T = len(maters)
        md0, md1 = [], []
        for i in range(T):
            if maters[i].model == 0:
                md0.append(i)
            else:
                md1.append(i)
        model_05_new = []
        if len(model_05)>0:
            # 生成初始结果
            mod_x = []
            for mod in model_05:
                if (mod[-1].color_same == 1) & (mod[-2].model==mod[0].model):
                    mod_x.append(mod[-1])
                    if  (mod[0].model == 0):
                        mod = mod[:-1]
                    else:
                        mod = mod[:-1][::-1]
                elif (mod[-2].model==mod[0].model):
                    if (mod[0].model == mod[-1].model) | (mod[0].model == 0):
                        mod = mod
                    else:
                        mod = mod[::-1]
                    model_05_new.append(mod)
                else:
                    model_05_new.append(mod)
                T = 0
                if mod[0].model != mod[-1].model:
                    pass
                elif len(mod)>0:
                    for mater in self.maters:
                        if mod[0].model == mater.model:
                            for mt in range(len(mater.order)):
                                mtorder = mater.order[mt]
                                try:
                                    if (mater.order[mt].derailleur == 0) & (mater.order[mt + 1].derailleur == 0) & (
                                            mater.order[mt].color_roof == 10) & (mater.order[mt + 1].color_roof == 10):
                                        self.insert_two_2(mater, mod, mt)
                                        T = 1
                                        break
                                except:
                                    pass
                            if T == 1:
                                break
                if len(mod_x) == len(model_05):
                    break
            for m in mod_x:
                if m.model == 0:
                    model_0.append(m)
                else:
                    model_1.append(m)
            # 生成初始结果
        model_05 = []
        if len(model_05_new)>0:
            T=1
            model_05=model_05_new
        result = []
        for me in md0:
            for od in maters[me].order:
                result.append(od.id)
        if len(model_0) > 0:
            for md in model_0:
                result.append(md.id)
        if len(model_05)==0: # 目标1不存在优化的区间,直接提交结果
            T=0
        elif len(model_05)==1:
            m=len(model_05)
            for m_ in range(m):
                md=model_05[m_]
                if (md[0].model==1) & (md[-1].model==0):
                    md=self.change_direction(md)
                for mdd in range(len(md)):
                    result.append(md[mdd].id)
        if len(model_1) > 0:
            for md in model_1:
                result.append(md.id)
        for me in md1:
            for od in maters[me].order:
                result.append(od.id)
        return result,T

    def variation(self,result0,check=True,NUM=500):
        res = []
        result = []
        N = 0
        while N < NUM:
            rs = random.sample(range(len(result0) - self.min_num), 2)
            if rs[1] - rs[0] > self.min_num:
                N += 1
                result1 = result0[:rs[0]] + result0[rs[1]:rs[1] + self.min_num] + result0[rs[0] + self.min_num:rs[1]] + result0[rs[0]: rs[0] + self.min_num] + result0[rs[1] + self.min_num:]
                res.append(result1)
        if check:
            res,Function = self.funcs(res, self.DATA)
            q_DominatedCount = self.NonDominatedSorting(Function)
            dic_v = dict(Counter(q_DominatedCount))
            dic1SortList = sorted(dic_v.items(), key=lambda x: x[0], reverse=False)
            Max_v = dic1SortList[0][0]
            for i in range(len(Function)):
                if q_DominatedCount[i] == Max_v:
                    result.append(res[i])
            if len(result) == 0:
                result.append(result0)
        else:
            result=result+res
        if len(result) == 0:
            result.append(result0)
        return result

    def NonDominatedSorting(self,Function):
        num=len(Function)
        q_DominatedCount=[0 for i in range(num)]
        for i in range(num):
            for j in range(i+1,num):
                x=(Function[i][0] <= Function[j][0]) & (Function[i][1] <= Function[j][1]) & (
                        Function[i][2] <= Function[j][2]) & (Function[i][3] <= Function[j][3])
                y= (Function[i][0] <= Function[j][0]) | (Function[i][1] <= Function[j][1]) | (
                        Function[i][2] <= Function[j][2]) | (Function[i][3] <= Function[j][3])
                x1 = (Function[j][0] <= Function[i][0]) & (Function[j][1] <= Function[i][1]) & (
                        Function[j][2] <= Function[i][2]) & (Function[j][3] <= Function[i][3])
                y1 = (Function[j][0] <= Function[i][0]) | (Function[j][1] <= Function[i][1]) | (
                        Function[j][2] <= Function[i][2]) | (Function[j][3] <= Function[i][3])
                if x & y:
                    q_DominatedCount[j]+=1
                if  x1 & y1:
                    q_DominatedCount[i]+=1

        return q_DominatedCount

    def sort_List(self,map_index):
        keys = list(map_index.keys())
        for i in range(len(keys)):
            for j in range(i):
                if (map_index[keys[i]][2] > map_index[keys[j]][2]):
                    t = map_index[keys[i]]
                    map_index[keys[i]] = map_index[keys[j]]
                    map_index[keys[j]] = t
        for i in range(len(keys)):
            for j in range(i):
                if (map_index[keys[i]][4] == True) & (map_index[keys[j]][4] == False):
                    t = map_index[keys[i]]
                    map_index[keys[i]] = map_index[keys[j]]
                    map_index[keys[j]] = t
        return map_index

    def sort_result(self,res,F):
        result=[]
        for j in range(len(res)):
            res0=res[j]
            new_data = pd.DataFrame(columns=self.DATA.columns.values)
            for i in range(len(res0)):
                new_data.loc[i, :] = self.DATA[self.DATA['id'] == res0[i]].values[0]
            change_index,_ = obj_1_new(res0, new_data,F[j])
            # if self.Sort_i==0:
            change_index = obj_3_new(change_index, new_data)
            new_data = pd.DataFrame(columns=self.DATA.columns.values)
            for i in range(len(change_index)):
                new_data.loc[i, :] = self.DATA[self.DATA['id'] == change_index[i]].values[0]
            result.append(change_index)
        return result

    def local_deal(self,result0,T):
        result=[]
        result.append(result0)
        new_data = pd.DataFrame(columns=self.DATA.columns.values)
        for i in range(len(result0)):
            new_data.loc[i, :] = self.DATA[self.DATA['id'] == result0[i]].values[0]
        obj2, map_index = obj_2_old(result0, self.DATA)
        map_index = self.sort_List(map_index)
        map_ind = []
        for mp in map_index.values():
            map_ind.append(mp[1])
        count=0
        for k in range(len(result0)):
            temp1 = new_data[new_data['id'] == result0[k]]
            if (temp1.model.values[0] == 1):
                k-=1
                for j in range(k, -1, -1):
                    temp = new_data[new_data['id'] == result0[j]]
                    if (temp.color_same.values[0] == 0):
                        count+=1
                    else:
                        break
                break
        if len(self.Parateo)>0:
            for P in self.Parateo:
                for i in range(len(result0)):
                    if result0[i]==P:
                        for j in range(i,-1,-1):
                            temp=new_data[new_data['id'] == result0[j]]
                            if (temp.color_same.values[0]==0) & (temp.derailleur.values[0]==0):
                                count += 1
                                result0=result0[:j]+result0[j+1:k+1]+result0[j:j+1]+result0[k+1:]
                                new_data = pd.DataFrame(columns=self.DATA.columns.values)
                                for i in range(len(result0)):
                                    new_data.loc[i, :] = self.DATA[self.DATA['id'] == result0[i]].values[0]
                                if count==5:
                                    count=0
                                    for j in range(k,-1,-1):
                                        temp = new_data[new_data['id'] == result0[j]]
                                        temp1 = new_data[new_data['id'] == result0[j-1]]
                                        if (temp.color_roof.values[0]==10) & (temp1.color_roof.values[0]==10):
                                            result0 = result0[:j] + result0[j + 1:k+1] + result0[j:j + 1] + result0[k+1:]
                                            new_data = pd.DataFrame(columns=self.DATA.columns.values)
                                            for i in range(len(result0)):
                                                new_data.loc[i, :] = self.DATA[self.DATA['id'] == result0[i]].values[0]
                                            result.append(result0)
                                            break
                                else:
                                    result.append(result0)
                                break
                        break
        result_1=[]
        for result0 in result:
            new_data = pd.DataFrame(columns=self.DATA.columns.values)
            for i in range(len(result0)):
                new_data.loc[i, :] = self.DATA[self.DATA['id'] == result0[i]].values[0]
            obj2, map_index = obj_2_old(result0, self.DATA)
            map_index = self.sort_List(map_index)
            map_ind = []
            for mp in map_index.values():
                map_ind.append(mp[1])
            map_indexs = []
            for i in list(set(map_ind)):
                if map_ind.count(i)>1:
                    map_indexs.append(i)
            temp=[]
            temp.append(result0)
            m=0
            while (m<len(map_indexs)):
                v=[]
                if map_indexs[m]!=6:
                    for i in map_index.values():
                        if i[1]==map_indexs[m]:
                            v.append(i)
                    # 存在优化的空间
                    new_data1 = pd.DataFrame(columns=self.DATA.columns.values)
                    for i in v:
                        t=new_data.loc[i[0]-i[2]:i[0]-1]
                        new_data1=pd.concat([new_data1,t])
                        new_data1.sort_values(by=['model'],axis = 0,ascending = True,inplace=True)
                        new_data1=new_data1.reset_index(drop=True)
                    if T==0:
                        T=1
                        new_data2=new_data[~new_data['id'].isin(new_data1['id'])].reset_index(drop=True)
                        if new_data1.loc[0].model == 0:
                            for j in [i for i in range(k, -1, -1)] + [i for i in range(k + 1, new_data2.shape[0])]:
                                if (new_data2.loc[j].color_roof == 10) & (new_data2.loc[j + 1].color_roof == 10) & (new_data2.loc[j].color_body == map_indexs[m]):
                                    new_data = pd.concat([new_data2[:j + 1], new_data1, new_data2[j + 1:]]).reset_index(drop=True)
                                    temp.append(new_data.id.values.tolist())
                                    # if new_data1.shape[0] >5:
                                    #     if new_data1.loc[5].model==0:
                                    #         for j1 in [i for i in range(j-1, -1, -1)]:
                                    #             if (new_data.loc[j1].color_roof == 10) & (new_data.loc[j1 - 1].color_roof == 10) & (new_data.loc[j1].color_body == map_indexs[m]):
                                    #                 t1, t2, t3, t4 = new_data[:j + 6], new_data[j1:j1 + 1], new_data[j + 5:j + num], new_data[num:]
                                    #                 new_data = pd.concat([t1, t2, t3, t4]).reset_index(drop=True)
                                    #                 temp.append(new_data.id.values.tolist())
                                    #                 print('检测')
                                    #                 break
                                    #     else:
                                    #         for j1 in [i for i in range(k+1,new_data.shape[0])]+[i for i in range(k,-1,-1)]:
                                    #             if (j!=j1) & (new_data.loc[j1].color_roof == 10) & (new_data.loc[j1 + 1].color_roof == 10) & (new_data.loc[j1].color_body == map_indexs[m]):
                                    #                 new_data = pd.concat([new_data2[:j1 + 1], new_data1[:5], new_data2[j:j + 1],new_data1[5:], new_data2, new_data2[j + 1:]]).reset_index(drop=True)
                                    #                 temp.append(new_data.id.values.tolist())
                                    #                 print('检测')
                                    #                 break
                                    k += new_data1.shape[0]
                                    obj2, map_index = obj_2_old(new_data.id.values.tolist(), self.DATA)
                                    break
                    else:
                        new_data2 = new_data[~new_data['id'].isin(new_data1['id'])].reset_index(drop=True)
                        if new_data1.loc[0].model==0:
                            for j in [i for i in range(k,-1,-1)]+[i for i in range(k+1,new_data2.shape[0])]:
                                if (new_data2.loc[j].color_roof == 10) & (new_data2.loc[j+1].color_roof == 10) & (new_data2.loc[j].color_body==map_indexs[m]):
                                    new_data = pd.concat([new_data2[:j + 1], new_data1, new_data2[j + 1:]]).reset_index(drop=True)
                                    temp.append(new_data.id.values.tolist())
                                    # if new_data1.shape[0] >5:
                                    #     if new_data1.loc[5].model==0:
                                    #         for j1 in [i for i in range(j-1, -1, -1)]:
                                    #             if (new_data.loc[j1].color_roof == 10) & (new_data.loc[j1 - 1].color_roof == 10) & (new_data.loc[j1].color_body == map_indexs[m]):
                                    #                 t1, t2, t3, t4 = new_data[:j + 6], new_data[j1:j1 + 1], new_data[j + 5:j + num], new_data[num:]
                                    #                 new_data = pd.concat([t1, t2, t3, t4]).reset_index(drop=True)
                                    #                 temp.append(new_data.id.values.tolist())
                                    #                 print('检测')
                                    #                 break
                                    #     else:
                                    #         for j1 in [i for i in range(k+1,new_data.shape[0])]+[i for i in range(k,-1,-1)]:
                                    #             if (j!=j1) & (new_data.loc[j1].color_roof == 10) & (new_data.loc[j1 + 1].color_roof == 10) & (new_data.loc[j1].color_body == map_indexs[m]):
                                    #                 new_data = pd.concat([new_data2[:j1 + 1], new_data1[:5], new_data2[j:j + 1],new_data1[5:], new_data2, new_data2[j + 1:]]).reset_index(drop=True)
                                    #                 temp.append(new_data.id.values.tolist())
                                    #                 print('检测')
                                    #                 break
                                    k+=new_data1.shape[0]
                                    obj2, map_index = obj_2_old(new_data.id.values.tolist(), self.DATA)
                                    break
                        else:
                            for j in [i for i in range(k+1,new_data2.shape[0])]+[i for i in range(k,-1,-1)]:
                                if (new_data2.loc[j].color_roof == 10) & (new_data2.loc[j+1].color_roof == 10) & (new_data2.loc[j].derailleur == 0) & (new_data2.loc[j+1].derailleur == 0) & (new_data2.loc[j].color_body==map_indexs[m]):
                                    new_data = pd.concat([new_data2[:j + 1], new_data1, new_data2[j + 1:]]).reset_index(drop=True)
                                    temp.append(new_data.id.values.tolist())
                                    # if new_data1.shape[0] >5:
                                    #     if new_data1.loc[5].model == 0:
                                    #         for j1 in [i for i in range(j - 1, -1, -1)] :
                                    #             if (new_data.loc[j].color_roof == 10) & (new_data.loc[j + 1].color_roof == 10) & (new_data.loc[j].color_body == map_indexs[m]):
                                    #                 t1, t2, t3, t4 = new_data[:j + 6], new_data[j1:j1 + 1], new_data[j + 5:j + num], new_data[num:]
                                    #                 new_data = pd.concat([t1, t2, t3, t4]).reset_index(drop=True)
                                    #                 temp.append(new_data.id.values.tolist())
                                    #                 print('检测')
                                    #                 break
                                    #     else:
                                    #         for j1 in [i for i in range(j + 1, new_data2.shape[0])] :
                                    #             num=new_data1.shape[0]
                                    #             if  (new_data.loc[j1].color_roof == 10) & (new_data.loc[j1 - 1].color_roof == 10) & (new_data.loc[j1].color_body == map_indexs[m]):
                                    #                 t1,t2,t3,t4=new_data[:j +6],new_data[j1:j1 + 1],new_data[j +5:j+num], new_data[num:]
                                    #                 new_data = pd.concat([t1,t2,t3,t4]).reset_index(drop=True)
                                    #                 temp.append(new_data.id.values.tolist())
                                    #                 print('检测')
                                    #                 break
                                    k += new_data1.shape[0]
                                    obj2, map_index = obj_2_old(new_data.id.values.tolist(), self.DATA)
                                    break
                else:
                    for i in map_index.values():
                        if (i[1] == map_indexs[m]) & ((i[0]<k) | (i[0]>=k+5)):
                            v.append(i)
                    # 存在优化的空间
                    new_data1 = pd.DataFrame(columns=self.DATA.columns.values)
                    for i in v:
                        t = new_data.loc[i[0] - i[2]:i[0] - 1]
                        new_data1 = pd.concat([new_data1, t])
                    new_data2 = new_data[~new_data['id'].isin(new_data1['id'])].reset_index(drop=True)
                    result0=new_data.id.values.tolist()
                    for k in range(len(result0)):
                        temp1 = new_data[new_data['id'] == result0[k]]
                        if (temp1.model.values[0] == 1) & (temp1.color_body.values[0] == 6):
                            k -= 1
                            break
                    new_data = pd.concat([new_data2[:k -1], new_data1, new_data2[k -1:]])
                    temp.append(new_data.id.values.tolist())
                    k += new_data1.shape[0]
                    obj2, map_index = obj_2_old(new_data.id.values.tolist(), self.DATA)
                    # 添加10，形成非支配解
                    # if new_data1.shape[0] > 5:
                    #     if new_data1.loc[5].model == 0:
                    #         for j1 in [i for i in range(j - 1, -1, -1)]:
                    #             if (new_data.loc[j1].color_roof == 10) & (new_data.loc[j1 - 1].color_roof == 10) & (
                    #                     new_data.loc[j1].color_body == map_indexs[m]):
                    #                 t1, t2, t3, t4 = new_data[:j + 6], new_data[j1:j1 + 1], new_data[
                    #                                                                         j + 5:j + num], new_data[
                    #                                                                                         num:]
                    #                 new_data = pd.concat([t1, t2, t3, t4]).reset_index(drop=True)
                    #                 temp.append(new_data.id.values.tolist())
                    #                 print('检测')
                    #                 break
                    #     else:
                    #         for j1 in [i for i in range(k + 1, new_data2.shape[0])] + [i for i in range(k, -1, -1)]:
                    #             if (j != j1) & (new_data2.loc[j].color_roof == 10) & (
                    #                     new_data2.loc[j + 1].color_roof == 10) & (
                    #                     new_data2.loc[j].color_body == map_indexs[m]):
                    #                 new_data = pd.concat(
                    #                     [new_data2[:j1 + 1], new_data1[:5], new_data2[j:j + 1], new_data1[5:],
                    #                      new_data2, new_data2[j + 1:]]).reset_index(drop=True)
                    #                 temp.append(new_data.id.values.tolist())
                    #                 print('检测')
                    #                 break
                m+=1
            if len(temp)==1:
                result_1.append(temp[0])
            else:
                for t in temp:
                    result_1.append(t)
        #删除无用结果
        result, Function = self.funcs(result_1, self.DATA)
        if len(result) > 1:
            res = []
            F=[]
            # q_DominatedCount = self.NonDominatedSorting(Function)
            # dic_v = dict(Counter(q_DominatedCount))
            # dic1SortList = sorted(dic_v.items(), key=lambda x: x[0], reverse=False)
            # Max_v = dic1SortList[0][0]
            # for i in range(len(Function)):
            #     if q_DominatedCount[i] == Max_v:
            #         res.append(result[i])
            #         F.append(Function[i])
            # if len(res) == 0:
            #     res.append(result[0])
            # #优化序列，将长度<23的序列补齐
            # result=self.sort_result(res,F)
            result = self.sort_result(result, Function)
            return result
        else:
            result = self.sort_result(result,Function)
        return result

    #去重
    def deduplicate(self,Func,result):
        Func_ = list(set(Func))
        i = 0
        Result = []
        result_func = []
        while i < len(Func_):
            Func_i = Func_[i]
            for j in range(len(Func)):
                Func_j = Func[j]
                if Func_j == Func_i:
                    Result.append(result[j])
                    result_func.append(Func_[i])
                    i += 1
                    break
        return Result,result_func

    def funcs(self,result,data):
        Func=[]
        for rs in result:
            obj1 = obj_1(rs, data)
            obj2, _ = obj_2(rs, data)
            obj3 = obj_3(rs, data)
            obj4_qi, _ = obj_2_old(rs, data)
            obj4 = obj_4(rs, data, obj4_qi)
            Func.append((obj1,obj2,obj3,obj4))
        # Result,result_func=self.deduplicate(Func, result)
        # return Result,result_func
        return  result,Func

    def start(self):
        for bin in self.bins:
            score = 0
            for mater in self.maters:
                s = mater.find_mater(bin)
                if s:
                    mater.insert(bin)
                    mater.common += bin.common_2 + bin.common_4
                    mater.num += bin.num
                    mater.end_color=bin.items[-1].color_body
                    score = 1
                    break
            if score == 0:
                new_mater = self._mater_factory(self.min_num)
                new_mater.insert(bin)
                new_mater.set_v(bin)
                self.maters.append(new_mater)
        self.maters.sort(key=lambda x: x.num, reverse=True)
        model_0,model_05, model_1 = [], [],[]
        i = -1
        while i < len(self.maters):
            i += 1
            try:
                mater = self.maters[i]
                if (mater.num<self.min_num) :
                    if (mater.model!=0.5) & (mater.num>5):
                        for j in range(i + 1, len(self.maters)):
                            old_mater = self.maters[j]
                            if (old_mater.model == mater.model) :
                                self.change_two_2(mater, old_mater)
                                self.maters.remove(old_mater)
                            if mater.num>self.min_num:
                                break
                    elif mater.model == 0.5:
                        model_05.append(mater.order)
                        self.maters.remove(mater)
                        i -= 1
                    elif mater.num==1:
                        if mater.model==0:
                            model_0.append(mater.order[0])
                            self.maters.remove(mater)
                        elif mater.model==1:
                            model_1.append(mater.order[0])
                            self.maters.remove(mater)
                        i-=1
            except:
                pass
        result0,T = self.submit(self.maters, model_0, model_1,model_05) #先简单处理
        if self.TYPE == 0:
            return [result0]
        ###基于深度查找，一旦查找到更优解。以此为基础深度查找
        elif self.TYPE==1:      #1--47
            result=self.local_deal(result0,T)
            return result
        elif self.TYPE==2:       #2--46
            result = self.variation(result0,check=True,NUM=50)    #NUM值设置太大，会使产生的解较差
            return result
        elif self.TYPE == 3:       #--14
            result_data=self.local_deal(result0)
            end_time=time.time()    #结束计时
            Max_result=result_data
            result_old=[]
            Function_old=[]
            while (len(result_data)<20) & ((end_time-self.time_start)<3600):
                print('当前种群个数：'+str(len(result_data))+'   '+'已消耗时间：'+str(end_time-self.time_start))
                result = result_data
                for res in result_data:
                    resu = self.variation(res,check=False,NUM=int(50))
                    result=result+resu
                result_data=[]
                result,Function = self.funcs(result, self.DATA)
                if len(Function)>0:
                    result=result+result_old
                    Function=Function+Function_old
                    if len(result_old)>0:
                        result, Function =self.deduplicate(Function, result)
                print('总个数数量：' + str(len(result)))
                result_old=result
                Function_old=Function
                q_DominatedCount = self.NonDominatedSorting(Function)
                dic_v = dict(Counter(q_DominatedCount))
                dic1SortList = sorted(dic_v.items(), key=lambda x: x[1], reverse=True)
                Max_v = dic1SortList[0][0]
                # for i in range(len(Function)):
                #     if dic1SortList[i][1] > 1:
                #         Max_v = dic1SortList[i][0]
                #         break
                for i in range(len(Function)):
                    if q_DominatedCount[i] == Max_v:
                        result_data.append(result[i])
                        # print(Function[i])
                if len(result_data) == 0:
                    result_data=result_data
                end_time = time.time()  # 结束计时
                if len(result_data)>len(Max_result):
                    Max_result=result_data
                if len(result)>1000:
                    break
            return Max_result






