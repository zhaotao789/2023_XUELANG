import pandas as pd
from First_seq import *
from weld import *
from obj import *
import os
common_value=[]
from tqdm import tqdm
from multiprocessing.pool import Pool, ThreadPool
import time
#将表格直接生成图片
from pandas.plotting import  table
import matplotlib.pyplot as plt
# plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']#显示中文字体
import random
def get_result(file):

    data = pd.read_csv('数据集/{}'.format(file))  #('数据集/data_103.csv')#
    d = file.split('.')[0]
    re = pd.read_excel('作品上传示例.xlsx', sheet_name='{}'.format(d))
    result1 = re[['Variable {}'.format(i) for i in range(1, int(d.split('_')[1]) + 1)]]
    #result1 = result1 + 1
    result1.drop(result1.index, inplace=True)

    time_start = time.time()  # 开始计时
    models = {
        'A': 0,
        'B': 1
    }
    body_color = {
        '薄雾灰': 0,
        '天空灰': 1,
        '飞行蓝': 2,
        '水晶紫': 3,
        '水晶珍珠白': 4,
        '明亮红': 5,
        '闪耀黑': 6,
        '探索绿': 7,
        '液态灰': 8,
        '黑曜黑': 9,
        '石黑': 10
    }
    drives_number = {
        '两驱': 0,
        '四驱': 1
    }
    Max_drive = 2
    data['id'] = data.index + 1
    data = data[['id', '车型', '车身颜色', '车顶颜色', '变速器']]
    data.columns = ['id', 'model', 'color_body', 'color_roof', 'derailleur']


    def roof(rows):
        if rows.color_roof == '无对比颜色':
            return rows.color_body
        else:
            return rows.color_roof


    def same_color(rows):
        if rows.color_roof == rows.color_body:
            return 0
        else:
            return 1


    data['color_roof'] = data.apply(roof, axis=1)
    data['color_same'] = data.apply(same_color, axis=1)
    data['model'] = data['model'].map(models)
    data['color_body'] = data['color_body'].map(body_color)
    data['color_roof'] = data['color_roof'].map(body_color)
    data['derailleur'] = data['derailleur'].map(drives_number)
    match_list = set(data[data['color_roof'] == 10]['color_body'].values)
    data.sort_values(by=['color_roof'], ascending=[0], inplace=True)  # 先对颜色排序   1表示顺序   0表示倒序
    # 找出车顶和车身不同的数据
    derailleur_4_de = data[(data['derailleur'] == 1) & (data['color_same'] == 1)]
    derailleur_4_com = data[(data['derailleur'] == 1) & (data['color_same'] == 0)]
    derailleur_2_de = data[(data['derailleur'] == 0) & (data['color_same'] == 1)]
    derailleur_2_com = data[(data['derailleur'] == 0) & (data['color_same'] == 0)]
    Parateo=data[(data['color_roof'] != 10) & (data['color_same'] == 1)]
    if Parateo.shape[0]>0:
        Parateo=list(Parateo.id.values)
    else:
        Parateo=[]
    result=[]
    for Sort_i in [1]:
        for Sort_j in [1]:
            fs = First_seq(derailleur_4_de, derailleur_4_com, derailleur_2_de, derailleur_2_com, Max_drive,Sort_i,Sort_j)
            bins = fs.start()
            # 排序
            wd = weld(bins, data, match_list, 0,time_start,Sort_i,Parateo)
            res = wd.start()
            result=result+res
    # result, Function = wd.funcs(result, data)
    if len(result) == 1:
        result = result[0]
        obj1 = obj_1(result, data)
        # 位置：颜色，个数，模式，是否可以移动
        obj2, _ = obj_2(result, data)
        print('共找到个体个数：1')
        obj3 = obj_3(result, data)
        obj4_qi, map_index = obj_2_old(result, data)
        obj4 = obj_4(result, data, obj4_qi)
        # print(map_index)
        print('目标四理论换漆最优值：' + str(data[data['color_roof'] > 8].shape[0] + data[data['color_same'] == 1].shape[0]))
        # print('目标四实际换漆次数'+str(obj4_qi))
        print('目标二优化最优值：' + str(-1*obj2) + '     ' + '目标一优化最优值：' + str(obj1) + '     ' + '目标三优化最优值：' + str(
            obj3) + '     ' + '目标四优化最优值：' + str(obj4))
        result1.loc[0] = result
    elif len(result) > 1:
        print('共找到个体个数：' + str(len(result)))
        print('目标四理论换漆最优值：' + str(data[data['color_roof'] > 8].shape[0] + data[data['color_same'] == 1].shape[0]))
        for i in range(len(result)):
            obj1 = obj_1(result[i], data)
            # 位置：颜色，个数，模式，是否可以移动
            obj2, _ = obj_2(result[i], data)
            obj3 = obj_3(result[i], data)
            obj4_qi, map_index = obj_2_old(result[i], data)
            obj4 = obj_4(result[i], data, obj4_qi)
            # print(map_index)
            # print('目标四实际换漆次数' + str(obj4_qi))
            print('目标二优化最优值：' + str(-1*obj2) + '     ' + '目标一优化最优值：' + str(obj1) + '     ' + '目标三优化最优值：' + str(
                obj3) + '     ' + '目标四优化最优值：' + str(obj4))
            result1.loc[i] = result[i]
    return result1

if __name__ == '__main__':
    for _,_,files in os.walk('数据集'):
        outputfile = pd.ExcelWriter(r'test_sunqin.xlsx')

        # NUM_THREADS=4
        # results = ThreadPool(NUM_THREADS).imap(get_result, files)
        # pbar = tqdm(enumerate(results), total=100,  disable=False)
        # for i, x in pbar:
        #     d1 = x
        #     d1 = d1 - 1
        #     d1.to_excel(outputfile, sheet_name='data_{}'.format(x.shape[1]), index=False)
        # outputfile.save()
        # outputfile.close()
        # files=files[23:]
        for file in tqdm(files):
            result1=get_result(file)
            d1 = result1
            d1 = d1 - 1
            d1.to_excel(outputfile, sheet_name=file.split('.')[0], index=False)
        outputfile.save()
        outputfile.close()
