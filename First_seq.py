from seq_box import *
import pandas as pd
class First_seq:
    def __init__(self,derailleur_4_de, derailleur_4_com, derailleur_2_de, derailleur_2_com,Max_drive,Sort_i,Sort_j):
        self.derailleur_4_de=derailleur_4_de
        self.derailleur_4_com=derailleur_4_com
        self.derailleur_2_de = derailleur_2_de
        self.derailleur_2_com = derailleur_2_com
        self.Max_drive=Max_drive
        self.bins=[]
        self.Sort_j=Sort_j
        self.Sort_i = Sort_i

    def _bin_factory(self,max_drive,common_2=0,common_4=0,def_2=0,def_4=0):
        return seq_box(max_drive=max_drive,common_2=common_2,common_4=common_4,def_2=def_2,def_4=def_4)



    def change_four(self,a, b):
        item = b.items[-1]
        a.insert(item)
        b.items =[]
        a.def_4 += 1
        a.num+=1

    def change_four_com(self,a, b):
        item = a.items[-1]
        b.insert(item)
        a.items =a.items[:-1]
        a.common_4-= 1
        a.num-=1
        b.common_4 += 1
        b.num += 1

    def change_two(self,a, b):
        item = b.items[-1]
        a.items.insert(0,item)
        b.items =[]
        a.def_2 += 1
        a.num+=1

    def change_two_2(self,a, b):
        if len(b.items)==1:
            item = b.items[-1]
            a.insert(item)
            b.items =[]
            a.def_2 += 1
            a.num+=1
        else:
            for i in b.items:
                a.insert( i)
                a.num += 1
                a.def_2 += 1

    def change_two_1(self,a, b):
        for i in b.items :
            a.items.insert(0,i)
            a.num+=1

    def change_inter(self,bin, index):
        if index==2:
            t=bin.items[1]
            bin.items[1]=bin.items[0]
            bin.items[0]=t
        if index==3:
            t=bin.items[0]
            bin.items[0]=bin.items[2]
            bin.items[2]=t
        if index==1:
            pass

    def change_direction(self,bin):
        items=bin.items
        new_items=[]
        for i in range(len(items)-1,-1,-1):
            new_items.append(items[i])
        bin.items=new_items

    def two_common(self):
        max_drive=5
        f=self.derailleur_2_com
        f.sort_values(by=['color_roof'], inplace=True)
        for i in range(f.shape[0]):
            item = f.iloc[i]
            score = 0
            for bin in self.bins:
                # 找出最适合的bin
                if self.Sort_i == 0:
                    s = bin.find_two_common_box(item)
                else:
                    s = bin.find_two_common_box_1(item)
                if s:
                    bin.insert(item)
                    bin.common_2+=1
                    bin.num+=1
                    score = 1
                    break
            if score == 0:
                new_bin = self._bin_factory(max_drive)
                new_bin.insert(item)
                new_bin.set_color(item,1)
                self.bins.append(new_bin)
        self.bins.sort(key=lambda x: x.num, reverse=True)
        i = -1
        while i < len(self.bins):
            i += 1
            try:
                bin = self.bins[i]
                if self.Sort_j==0:
                    # 判断是否需要更换位置
                    if (bin.items[0].derailleur==1) & (bin.common_2>0)  & (bin.def_4>0) & (bin.items[0].color_body==bin.items[-1].color_roof):
                        self.change_inter(bin,bin.def_4+bin.common_4)
                    if bin.sort_Y:
                        self.change_direction(bin)
                    if (bin.num >= 5):   #底部添加一个，起过滤作用
                        T=0
                        for j in range(i+1,len(self.bins)):
                            old_bin = self.bins[j]
                            if (old_bin.model == bin.model) & (old_bin.top_color == 10)  & (old_bin.num == 1):
                                self.change_two_2(bin,old_bin)
                                self.bins.remove(old_bin)
                                T=1
                                break
                        if T==0:
                            for j in range(i + 1, len(self.bins)):
                                old_bin = self.bins[j]
                                if  (old_bin.top_color == 10) & (old_bin.num == 1):
                                    self.change_two_2(bin, old_bin)
                                    self.bins.remove(old_bin)
                                    bin.model=0.5
                                    break
                    elif (bin.common_2+bin.common_4>0):
                        for j in range(i + 1, len(self.bins)):
                            old_bin = self.bins[j]
                            if (old_bin.items[0].color_roof==bin.items[-1].color_body) : #& (old_bin.common_4+old_bin.common_2+bin.common_4+bin.common_2<6)
                                self.change_two_2(bin, old_bin)
                                self.bins.remove(old_bin)
                                bin.model=0.5
                            if bin.num>4:
                                break
                        for k in range(i + 1, len(self.bins)):
                            old_bin = self.bins[k]
                            if (old_bin.model == bin.items[-1].model) & (old_bin.top_color == 10) & (old_bin.num == 1):
                                self.change_two_2(bin, old_bin)
                                self.bins.remove(old_bin)
                                break
                    elif (bin.common_4+bin.def_4>1):    #对于不满足栈的序列，先随机排序，后面再优化
                        T=0
                        for j in range(i+1,len(self.bins)):
                            old_bin = self.bins[j]
                            if (old_bin.model == bin.model)  & (old_bin.num <3) & (old_bin.items[0].derailleur==0):
                                self.change_two_2(bin,old_bin)
                                self.bins.remove(old_bin)
                                T=1
                                break
                        if T==0:
                            for j in range(i + 1, len(self.bins)):
                                old_bin = self.bins[j]
                                if  (old_bin.top_color == 10) & (old_bin.num == 1):
                                    self.change_two_2(bin, old_bin)
                                    self.bins.remove(old_bin)
                                    bin.model=0.5
                                    break
                    elif (bin.num>1):
                        T=0
                        for j in range(i+1,len(self.bins)):
                            old_bin = self.bins[j]
                            if (old_bin.model == bin.model)  & (old_bin.top_color == 10) & (old_bin.num == 1):
                                self.change_two_2(bin,old_bin)
                                self.bins.remove(old_bin)
                                T=1
                                break
                        if T==0:
                            for j in range(i + 1, len(self.bins)):
                                old_bin = self.bins[j]
                                if  (old_bin.top_color == 10) & (old_bin.num == 1):
                                    self.change_two_2(bin, old_bin)
                                    self.bins.remove(old_bin)
                                    bin.model=0.5
                                    break
                elif self.Sort_j == 1:  # 无效
                    # 判断是否需要更换位置
                    if (bin.items[0].derailleur == 1) & (bin.common_2 > 0) & (bin.def_4 > 0) & (
                            bin.items[0].color_body == bin.items[-1].color_roof):
                        self.change_inter(bin, bin.def_4 + bin.common_4)
                    if bin.sort_Y:
                        self.change_direction(bin)
                        if bin.items[-1].derailleur == 1:
                            for j in range(i + 1, len(self.bins)):
                                old_bin = self.bins[j]
                                if (old_bin.model == bin.model) & (old_bin.top_color == 10) & (old_bin.num == 1) & (
                                        old_bin.items[0].derailleur == 0):
                                    self.change_two(bin, old_bin)
                                    self.bins.remove(old_bin)
                                    break
                            for j in range(i + 1, len(self.bins)):
                                old_bin = self.bins[j]
                                if (old_bin.model == bin.model) & (old_bin.top_color == 10) & (old_bin.num == 1) & (
                                        old_bin.items[0].derailleur == 0):
                                    self.change_two_2(bin, old_bin)
                                    self.bins.remove(old_bin)
                                    break
                    elif (bin.common_4 + bin.common_2 == bin.num):  # 是否可以头部添加一个
                        T = -1
                        for j in range(i + 1, len(self.bins)):
                            old_bin = self.bins[j]
                            if (old_bin.def_4 == 3):
                                if (old_bin.model == bin.model) & (
                                        (old_bin.items[0].color_body == bin.items[0].color_roof) | (
                                        old_bin.items[1].color_body == bin.items[0].color_roof)):
                                    T += 1
                                    if (old_bin.items[0].color_body == bin.items[0].color_roof):
                                        item = old_bin.items[0]
                                        bin.items.insert(0, item)
                                        old_bin.items = old_bin.items[1:]
                                    else:
                                        item = old_bin.items[1]
                                        bin.items.insert(0, item)
                                        old_bin.items = old_bin.items[0:1] + old_bin.items[2:]
                                    bin.def_4 += 1
                                    old_bin.def_4 -= 1
                                    bin.num += 1
                                    old_bin.num -= 1
                            elif (old_bin.def_4 == 2):
                                if (old_bin.model == bin.model) & (
                                        old_bin.items[0].color_body == bin.items[0].color_roof):
                                    T += 1
                                    item = old_bin.items[0]
                                    bin.items.insert(0, item)
                                    old_bin.items = old_bin.items[1:]
                                    bin.def_4 += 1
                                    old_bin.def_4 -= 1
                                    bin.num += 1
                                    old_bin.num -= 1
                            if T == 1:
                                break
                        if (T == -1) | (T == 1):
                            pass
                        else:
                            for j in range(i + 1, len(self.bins)):
                                old_bin = self.bins[j]
                                if (old_bin.def_4 == 3) & (old_bin.model == bin.model):
                                    item = old_bin.items[0]
                                    bin.items.insert(0, item)
                                    old_bin.items = old_bin.items[1:]
                                    bin.def_4 += 1
                                    old_bin.def_4 -= 1
                                    bin.num += 1
                                    old_bin.num -= 1
                    if bin.common_4 + bin.common_2 == bin.num:  # 顶部添加一个，起过滤作用
                        T = 0
                        for j in range(i + 1, len(self.bins)):
                            old_bin = self.bins[j]
                            if (old_bin.model == bin.model) & (old_bin.top_color == 10) & (old_bin.num == 1) & (
                                    old_bin.items[0].derailleur == 0):
                                self.change_two(bin, old_bin)
                                self.bins.remove(old_bin)
                                T = 1
                                break
                        if T == 0:
                            for j in range(len(self.bins)):
                                old_bin = self.bins[j]
                                if (old_bin.model == bin.model) & (old_bin.items[0].derailleur == 0):
                                    self.change_two_2(bin, old_bin)
                                    self.bins.remove(old_bin)
                                    T = 1
                                    break
                        if T == 0:
                            for j in range(i + 1, len(self.bins)):
                                old_bin = self.bins[j]
                                if (old_bin.top_color == 10) & (old_bin.num == 1) & (old_bin.items[0].derailleur == 0):
                                    self.change_two(bin, old_bin)
                                    self.bins.remove(old_bin)
                                    bin.model = 0.5
                                    break
                    elif (bin.common_4 + bin.def_4 == bin.num):  # 对于不满足栈的序列，先随机排序，后面再优化
                        T = 0
                        for j in range(i + 1, len(self.bins)):
                            old_bin = self.bins[j]
                            if (old_bin.model == bin.model) & (old_bin.num == 1) & (old_bin.items[0].derailleur == 0):
                                self.change_two(bin, old_bin)
                                self.bins.remove(old_bin)
                                T = 1
                                break
                        if T == 0:
                            for j in range(len(self.bins)):
                                old_bin = self.bins[j]
                                if (old_bin.model == bin.model) & (old_bin.items[0].derailleur == 0):
                                    self.change_two_2(bin, old_bin)
                                    self.bins.remove(old_bin)
                                    T = 1
                                    break
                        if T == 0:
                            for j in range(i + 1, len(self.bins)):
                                old_bin = self.bins[j]
                                if (old_bin.top_color == 10) & (old_bin.num == 1) & (old_bin.items[0].derailleur == 0):
                                    self.change_two(bin, old_bin)
                                    self.bins.remove(old_bin)
                                    bin.model = 0.5
                                    break
                elif self.Sort_j == 2:  # 无效
                    if (bin.items[0].derailleur == 1) & (bin.common_2 > 0) & (bin.def_4 > 0) & (
                            bin.items[0].color_body == bin.items[-1].color_roof):
                        self.change_inter(bin, bin.def_4 + bin.common_4)
                    if bin.sort_Y:
                        self.change_direction(bin)
                        if bin.items[-1].derailleur == 1:
                            for j in range(i + 1, len(self.bins)):
                                old_bin = self.bins[j]
                                if (old_bin.model == bin.model) & (old_bin.top_color == 10) & (old_bin.num == 1) & (
                                        old_bin.items[0].derailleur == 0):
                                    self.change_two(bin, old_bin)
                                    self.bins.remove(old_bin)
                                    break
                            for j in range(i + 1, len(self.bins)):
                                old_bin = self.bins[j]
                                if (old_bin.model == bin.model) & (old_bin.top_color == 10) & (old_bin.num == 1) & (
                                        old_bin.items[0].derailleur == 0):
                                    self.change_two_2(bin, old_bin)
                                    self.bins.remove(old_bin)
                                    break
                    elif (bin.num >= 4) | (bin.common_4 + bin.def_4 == bin.num):
                        T = 0
                        for j in range(i + 1, len(self.bins)):
                            old_bin = self.bins[j]
                            if (old_bin.model == bin.model) & (old_bin.top_color == 10) & (old_bin.num == 1) & (
                                    old_bin.items[0].derailleur == 0):
                                self.change_two_2(bin, old_bin)
                                self.bins.remove(old_bin)
                                T = 1
                                break
                        if T == 0:
                            for j in range(len(self.bins)):
                                old_bin = self.bins[j]
                                if (old_bin.model == bin.model) & (old_bin.items[0].derailleur == 0):
                                    self.change_two_2(bin, old_bin)
                                    self.bins.remove(old_bin)
                                    T = 1
                                    break
                        if T == 0:
                            for j in range(i + 1, len(self.bins)):
                                old_bin = self.bins[j]
                                if (old_bin.top_color == 10) & (old_bin.num == 1) & (old_bin.items[0].derailleur == 0):
                                    self.change_two_2(bin, old_bin)
                                    self.bins.remove(old_bin)
                                    bin.model = 0.5
                                    break
                    elif (bin.common_2 + bin.common_4 > 0):
                        for j in range(i + 1, len(self.bins)):
                            old_bin = self.bins[j]
                            if (old_bin.items[0].color_roof == bin.items[-1].color_body):
                                self.change_two_2(bin, old_bin)
                                self.bins.remove(old_bin)
                                bin.model = 0.5
                            if bin.num > 4:
                                break
                        for k in range(i + 1, len(self.bins)):
                            old_bin = self.bins[k]
                            if (old_bin.model == bin.items[-1].model) & (old_bin.top_color == 10) & (
                                    old_bin.num == 1) & (old_bin.items[0].derailleur == 0):
                                self.change_two_2(bin, old_bin)
                                self.bins.remove(old_bin)
                                break
                    elif (bin.num > 1):
                        T = 0
                        for j in range(i + 1, len(self.bins)):
                            old_bin = self.bins[j]
                            if (old_bin.model == bin.model) & (old_bin.top_color == 10) & (old_bin.num == 1) & (
                                    old_bin.items[0].derailleur == 0):
                                self.change_two_2(bin, old_bin)
                                self.bins.remove(old_bin)
                                T = 1
                                break
                        if T == 0:
                            for j in range(len(self.bins)):
                                old_bin = self.bins[j]
                                if (old_bin.model == bin.model) & (old_bin.items[0].derailleur == 0):
                                    self.change_two_2(bin, old_bin)
                                    self.bins.remove(old_bin)
                                    T = 1
                                    break
                        if T == 0:
                            for j in range(i + 1, len(self.bins)):
                                old_bin = self.bins[j]
                                if (old_bin.top_color == 10) & (old_bin.num == 1) & (old_bin.items[0].derailleur == 0):
                                    self.change_two_2(bin, old_bin)
                                    self.bins.remove(old_bin)
                                    bin.model = 0.5
                                    break
                elif self.Sort_j == 3:  # 无效
                    # 判断是否需要更换位置
                    if (bin.items[0].derailleur == 1) & (bin.common_2 > 0) & (bin.def_4 > 0) & (
                            bin.items[0].color_body == bin.items[-1].color_roof):
                        self.change_inter(bin, bin.def_4 + bin.common_4)
                    if bin.sort_Y:
                        self.change_direction(bin)
                        if bin.items[-1].derailleur == 1:
                            for j in range(i + 1, len(self.bins)):
                                old_bin = self.bins[j]
                                if (old_bin.model == bin.model) & (old_bin.top_color == 10) & (old_bin.num == 1) & (
                                        old_bin.items[0].derailleur == 0):
                                    self.change_two(bin, old_bin)
                                    self.bins.remove(old_bin)
                                    break
                            for j in range(i + 1, len(self.bins)):
                                old_bin = self.bins[j]
                                if (old_bin.model == bin.model) & (old_bin.top_color == 10) & (old_bin.num == 1) & (
                                        old_bin.items[0].derailleur == 0):
                                    self.change_two_2(bin, old_bin)
                                    self.bins.remove(old_bin)
                                    break
                    elif (bin.items[0].color_same == 0) & (bin.num > 1):  # 底部添加一个，起过滤作用
                        T = 0
                        for j in range(i + 1, len(self.bins)):
                            old_bin = self.bins[j]
                            if (old_bin.model == bin.model) & (old_bin.top_color == 10) & (old_bin.num == 1) & (
                                    old_bin.items[0].derailleur == 0):
                                self.change_two_2(bin, old_bin)
                                self.bins.remove(old_bin)
                                T = 1
                                break
                        if T == 0:
                            for j in range(len(self.bins)):
                                old_bin = self.bins[j]
                                if (old_bin.model == bin.model) & (old_bin.items[0].derailleur == 0):
                                    self.change_two_2(bin, old_bin)
                                    self.bins.remove(old_bin)
                                    T = 1
                                    break
                        if T == 0:
                            for j in range(i + 1, len(self.bins)):
                                old_bin = self.bins[j]
                                if (old_bin.top_color == 10) & (old_bin.num == 1) & (old_bin.items[0].derailleur == 0):
                                    self.change_two_2(bin, old_bin)
                                    self.bins.remove(old_bin)
                                    bin.model = 0.5
                                    break
                    elif (bin.common_2 + bin.common_4 > 0):
                        for j in range(i + 1, len(self.bins)):
                            old_bin = self.bins[j]
                            if (old_bin.items[0].color_roof == bin.items[-1].color_body):
                                self.change_two_2(bin, old_bin)
                                self.bins.remove(old_bin)
                                bin.model = 0.5
                            if bin.num > 4:
                                break
                        for k in range(i + 1, len(self.bins)):
                            old_bin = self.bins[k]
                            if (old_bin.model == bin.items[-1].model) & (old_bin.top_color == 10) & (
                                    old_bin.num == 1) & (old_bin.items[0].derailleur == 0):
                                self.change_two_2(bin, old_bin)
                                self.bins.remove(old_bin)
                                break
                    elif (bin.common_4 + bin.def_4 == bin.num):  # 对于不满足栈的序列，先随机排序，后面再优化
                        T = 0
                        for j in range(i + 1, len(self.bins)):
                            old_bin = self.bins[j]
                            if (old_bin.model == bin.model) & (old_bin.items[0].derailleur == 0) & (
                                    old_bin.num == 1) & (old_bin.items[0].derailleur == 0):
                                self.change_two_2(bin, old_bin)
                                self.bins.remove(old_bin)
                                T = 1
                                break
                        if T == 0:
                            for j in range(len(self.bins)):
                                old_bin = self.bins[j]
                                if (old_bin.model == bin.model) & (old_bin.items[0].derailleur == 0):
                                    self.change_two_2(bin, old_bin)
                                    self.bins.remove(old_bin)
                                    T = 1
                                    break
                        if T == 0:
                            for j in range(i + 1, len(self.bins)):
                                old_bin = self.bins[j]
                                if (old_bin.top_color == 10) & (old_bin.num == 1) & (old_bin.items[0].derailleur == 0):
                                    self.change_two_2(bin, old_bin)
                                    self.bins.remove(old_bin)
                                    bin.model = 0.5
                                    break
            except:
                pass
        self.bins.sort(key=lambda x: x.num, reverse=True)


    def two_def(self):
        max_drive = 1
        f = self.derailleur_2_de
        f.sort_values(by=['color_roof'], inplace=True)
        Bins=[]
        for i in range(f.shape[0]):
            item = f.iloc[i]
            score = 0
            if score == 0:
                new_bin = self._bin_factory(max_drive)
                new_bin.insert(item)
                new_bin.set_color(item,2)
                # if self.Sort_i == 0:
                self.bins.append(new_bin)
                # elif self.Sort_i == 1:
                #     Bins.append(new_bin)
        # if self.Sort_i == 1:
        #     self.bins = Bins + self.bins
        self.bins.sort(key=lambda x: x.common_4, reverse=True)
        for bin in self.bins:
            bin.max_drive = 5

    def four_common(self): #将颜色相同的四驱车排序，并存入已有栈中。否则新建栈
        max_drive=3
        f=self.derailleur_4_com
        f.sort_values(by=['color_roof'], inplace=True)
        for i in range(f.shape[0]):
            item = f.iloc[i]
            score = 0
            for bin in self.bins:
                # 找出最适合的bin
                s = bin.find_four_common_box(item)
                if s:
                    bin.insert(item)
                    bin.common_4+=1
                    bin.num+=1
                    score = 1
                    break
            if score == 0:
                new_bin = self._bin_factory(max_drive)
                new_bin.insert(item)
                new_bin.set_color(item,3)
                self.bins.append(new_bin)
        self.bins.sort(key=lambda x: x.common_4, reverse=False)
        i=-1
        while i<len(self.bins):
            i += 1
            try:
                bin=self.bins[i]
                if (bin.num==1) :   #对于单独存在的个体，需要找到另一个个体
                    if (bin.def_4==1):
                        for j in range(i+1,len(self.bins)):
                            old_bin=self.bins[j]
                            if self.Sort_i == 0:
                                if (old_bin.model == bin.model) & (old_bin.common_4==0) & (old_bin.num<3):
                                    self.change_four(old_bin,bin)
                                    i-=1
                                    self.bins.remove(bin)
                                    break
                            else:
                                if (old_bin.model == bin.model) & (old_bin.common_4==0) & (old_bin.num<2):
                                    self.change_four(old_bin,bin)
                                    i-=1
                                    self.bins.remove(bin)
                                    break
                    else:
                        for j in range(i+1,len(self.bins)): #对于相同颜色的车，需要找到和其同色的车
                            old_bin=self.bins[j]
                            if (old_bin.model == bin.model) & (old_bin.top_color==bin.top_color)  &(old_bin.def_4==0) :
                                if (old_bin.num==3):
                                    self.change_four_com(old_bin, bin)
                                    i -= 1
                                    #self.bins.remove(bin)
                                    break
                                elif (old_bin.num==2):
                                    self.change_four(old_bin, bin)
                                    old_bin.common_4+=1
                                    old_bin.def_4 =0
                                    i -= 1
                                    self.bins.remove(bin)
                                    break
            except:
                pass
        self.bins.sort(key=lambda x: x.num, reverse=False)
        while (self.bins[0].num==1) :  #可能还存在未匹配的单个个体，进行暴力匹配
            bin=self.bins[0]
            for j in range(1,len(self.bins)):
                old_bin = self.bins[j]
                if (old_bin.model == bin.model) & (old_bin.num <3):
                    for i in old_bin.items:
                        bin.insert(i)
                        bin.num += 1
                        if i.color_same==1:
                            bin.def_4 += 1
                        else:
                            bin.common_4 += 1
                    self.bins.remove(old_bin)
                    break
        self.bins.sort(key=lambda x: x.num, reverse=True)
        for bin in self.bins:
            bin.max_drive=1

    def four_def(self): #将不同颜色的四驱车按照颜色排列，每个栈仅存一个数据
        max_drive=1
        f=self.derailleur_4_de
        f.sort_values(by=['color_roof'],inplace=True)
        for i in range(f.shape[0]):
            item = f.iloc[i]
            score = 0
            if score == 0:
                new_bin = self._bin_factory(max_drive)
                new_bin.insert(item)
                new_bin.set_color(item,4)
                self.bins.append(new_bin)
        for bin in self.bins:
            bin.max_drive=3

    def start(self):
        self.four_def()
        self.four_common()
        self.two_def()
        self.two_common()
        return self.bins



