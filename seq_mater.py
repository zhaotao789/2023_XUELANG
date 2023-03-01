
class seq_mater:
    def __init__(self,max_num):
        self.num=0
        self.max_num = max_num
        self.model=-1
        self.end_color=-1
        self.start_color = -1
        self.order=[]

    def insert(self, fs):
        for f in fs.items:
            self.order.append(f)

    def set_v(self,bin):
        if self.model == -1:
            self.start_color=bin.items[0].color_roof
            self.end_color=bin.items[-1].color_body
            self.num+=bin.num
            self.current_num=bin.num
            self.model=bin.model
            self.common=bin.common_2+bin.common_4

    def find_mater(self,bin):
        if bin.model==0.5:
            return False
        if (bin.common_4+bin.def_4>0) & (bin.model==self.model):
            return True
        if (len(bin.items)>4) & (bin.items[-1].derailleur==0)& (len(self.order)>0) & (bin.model==self.model) & (self.num<self.max_num):
            return True
        else:
            return False

