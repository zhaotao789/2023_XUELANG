
class seq_box:
    # 生成焊接序列类  （车型，车身颜色，车顶颜色，车型更换次数，喷头颜色，喷头更换次数，四驱车连放个数）
    def __init__(self,max_drive=1,model=-1,common_2=0,common_4=0,def_2=0,def_4=0,body_color=0,top_color=0,num=0,four_num=0):
        self.model = model
        self.items=[]
        self.body_color =body_color
        self.top_color = top_color
        self.num=num
        self.max_drive=max_drive
        self.model=model
        self.common_2=common_2
        self.common_4 = common_4
        self.def_2 = def_2
        self.def_4 = def_4
        self.four_num=four_num
        self.sort_Y=False

    def insert(self, f):
        self.items.append(f)

    def set_color(self,item,index):
        if self.model == -1:
            self.body_color = item.color_body
            self.top_color = item.color_roof
            self.num += 1
            self.model = item.model
        if index==1:
            self.common_2+=1
        elif index == 2:
            self.def_2 += 1
        elif index == 3:
            self.common_4 += 1
        elif index == 4:
            self.def_4 += 1

    def find_two_common_box(self,item):
        if (item.model == self.model):
            if (self.common_2 + self.common_4 == self.num) & (
                    (self.top_color == item.color_body) | (self.body_color == item.color_body)) & (
                    self.num < self.max_drive):
                return True
            elif (self.def_4 + self.def_2 > 0):
                def_num = self.def_4 + self.def_2
                if (self.body_color == item.color_body) & (self.num - def_num < self.max_drive):
                    return True
                elif (self.top_color == item.color_body) & (self.num - def_num < self.max_drive):
                    self.sort_Y = True
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def find_two_common_box_1(self,item):
        if (item.model == self.model):
            if (self.common_2 + self.common_4 == self.num) & (
                    (self.top_color == item.color_body) | (self.body_color == item.color_body)) & (
                    self.num < self.max_drive):
                return True
            elif (self.def_4 + self.def_2 > 0):
                def_num = self.def_4 + self.def_2
                if (self.body_color == item.color_body) & (self.num - def_num < self.max_drive):
                    return True
                elif (self.top_color == item.color_body) & (self.num - def_num < self.max_drive - 1):
                    self.sort_Y = True
                    return True
                elif self.num==self.def_4:
                    if self.items[-1].color_body==item.color_body:
                        self.body_color=self.items[-1].color_body
                        self.top_color = self.items[-1].color_roof
                        return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def find_four_common_box(self,item):
        if  (item.model==self.model) & (self.num<self.max_drive) & ((item.color_body==self.body_color) | (self.top_color==item.color_body)):
                return True
        else:
            return False

    def find_two_de_box(self,item):
        if (len(self.items)>0) & (item.model==self.model):
            self.num = self.def_4 +self.common_4 + self.def_2
            if  (self.num<self.max_drive):
                return True
            else:
                return False
        else:
            return False

    def find_four_de_box(self,item):
        if  (item.model==self.model) & (self.num<self.max_drive):
                return True
        else:
            return False
