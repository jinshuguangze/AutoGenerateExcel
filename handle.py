import os
import random
import time

import pandas as pd

from pinyinlib import Pinyin

# 重置随机种子
random.seed(time.time())

# 读取原始表格
df = pd.read_table(os.path.dirname(__file__)+'/input.txt',sep='!',encoding='gbk',low_memory=False)

# 生成序号列表
serial = []
for i in range(0, df.shape[0]):
    serial.append(str(i+1).zfill(6))
dfo1 = pd.DataFrame({'序号': serial})

# 生成户名列表
name = df.loc[:, '客户信息平台姓名'].values.tolist()
dfo2 = pd.DataFrame({'户名': name})

# 生成证件类型列表
dfo3 = pd.DataFrame({'证件类型': ([10]*df.shape[0])})

# 生成证件号码列表
id_number = list(map(str, df.loc[:, '客户信息平台证件号码'].values.tolist()))
dfo4 = pd.DataFrame({'证件号码': id_number})

# 生成英文名
english_name = []
for i in name:
    english_name.append(Pinyin().get_pinyin_name(i, '', '', 'upper'))
dfo5 = pd.DataFrame({'英文名': english_name})

# 生成性别列表
gender = []
for i in id_number:
    # 如果是身份证号码，则生成性别
    if(len(i)==18):
        # 男：1，女：2，未知：0
        if(int(i[-2]) % 2 == 0):
            gender.append(2)
        else:
            gender.append(1)
    else:
        gender.append(0)
dfo6 = pd.DataFrame({'性别': gender})

# 生成国籍/地区列表
dfo7 = pd.DataFrame({'国籍/地区': (['CN']*df.shape[0])})

# 生成固定电话列表，注意生成的固定电话不带区号键“-”
landline = []
for i in list(map(str, df.loc[:, '固话'].values.tolist())):
    # 固定电话自带的情况
    if(i != 'nan'):
        # 将可能的区号键和小数去掉
        i = i.replace('-', '').replace('.0', '')
        # 如果长度为七，则插入区号0728，如果长度少一位或者多一位，则随机生成数字自动补全，分为带区号和不带区号两种情况，随机补全的电话尾部有“~”号
        if(len(i) == 7):
            landline.append('0728'+i)
        elif(len(i) == 6 or len(i) == 10):
            landline.append(i+str(random.randint(0, 9))+'~')
        elif(len(i) == 8 or len(i) == 12):
            landline.append(i[0:-1])
        else:
            landline.append(i)
    # 固定电话非自带的情况
    else:
        # 随机生成，经查证，目前只有城镇5开头和乡镇4开头的区分，故第一位只生成4或5，第二位生成非0，其余五位随机生成，随机生成的电话尾部有“~”号
        landline.append('0728'+str(random.randint(4, 5)) +
                        str(random.randint(1, 9))+str(random.randint(0, 99999)).zfill(5)+'~')
dfo8 = pd.DataFrame({'固定电话': landline})

# 生成手机号列表
phone_number=[]
for i in list(map(str, df.loc[:, '手机号'].values.tolist())):
    # 手机号自带的情况
    if(i!='nan'):
        phone_number.append(i)
    # 手机号不自带的情况
    else:
        phone_number.append('')
dfo9 = pd.DataFrame({'手机号': phone_number})

# 生成通讯地址列表
dfo10 = pd.DataFrame({'通讯地址': df.loc[:, '联系地址'].values.tolist()})

# 生成职业列表
career_list = [
    '49900~',
    '50100~',
    '50101~',
    '50102~',
    '50199~',
    '50200~',
    '50201~',
    '50202~',
    '50203~',
    '50204~',
    '50299~',
    '50300~',
    '50301~',
    '50302~',
    '50303~',
    '50399~',
    '50400~',
    '50401~',
    '50402~',
    '50403~',
    '50499~',
    '50500~',
    '50501~',
    '50502~',
    '50503~',
    '50504~',
    '50505~',
    '50506~',
    '50599~',
    '59900~',
    '60100~',
    '60101~'
]
career = []
for i in range(0, df.shape[0]):
    # 从职业列表中随机生成职业代码，随机生成出来的号码尾部有“~”号
    career.append(random.sample(career_list, 1)[0])
dfo11 = pd.DataFrame({'职业': career})

# 生成是否居住满一年列表
lived_full_year = []
for i in id_number:
    # 如果是身份证号码，则生成居住是否满一年
    if(len(i)==18):
        if(i[0:6] == '429006' or i[0:6] == '422428'):
            lived_full_year.append('1')
        else:
            lived_full_year.append('0')
    # 否则，生成“1”
    else:
        lived_full_year.append('1')
dfo12 = pd.DataFrame({'是否居住满一年': lived_full_year})

# 生成发证机关所在地代码列表
locate_code = []
for i in id_number:
    # 如果是身份证号码，则生成发证机关所在地代码
    if(len(i)==18):
        if(i[0:6] == '422428'):
            locate_code.append('429006')
        else:
            locate_code.append(i[0:6])
    # 否则，生成“429006”
    else:
        locate_code.append('429006')
dfo13 = pd.DataFrame({'发证机关所在地代码': locate_code})

# 生成证件有效截止日期列表
birthdate = []
for i in id_number:
    # 如果是身份证号码，则生成出生日期
    if(len(i)==18):
        birthdate.append(int(i[6:14]))
    else:
        birthdate.append(0)
turncate_date = []
n = -1
for i in list(map(str, df.loc[:, '证件到期日'].values.tolist())):
    n = n+1
    # 证件有效截止日期自带的情况
    if(i != 'nan'):
        i = i.replace('.0', '').replace(
            '年', '').replace('月', '').replace('日', '')
        # 没有过期
        if(int(i) >= 20200610):
            turncate_date.append(i)
        else:
            # 生日为空或90后，截止日期往后延10年，判断闰年情况
            if(birthdate[n]==0 or birthdate[n] >= 19900610):
                if(i[4:8] == '0229'):
                    years = int(i[0:4])+10
                    if (not((years % 4 == 0 and years % 100 != 0) or (years % 400 == 0))):
                        turncate_date.append(str(years)+'0301')
                        continue
                turncate_date.append(str(int(i)+100000))
            # 72-90年，截止日期往后延20年，判断闰年情况
            elif(birthdate[n] > 19720610 and birthdate[n] < 19900610):
                if(i[4:8] == '0229'):
                    years = int(i[0:4])+20
                    if (not((years % 4 == 0 and years % 100 != 0) or (years % 400 == 0))):
                        turncate_date.append(str(years)+'0301')
                        continue
                turncate_date.append(str(int(i)+200000))
            # 72年前，截止日期设为永久
            else:
                turncate_date.append('20991231')
    # 证件有效截止日期非自带的情况
    else:
        # 生日为空，则来自户口本信息，留空
        if(birthdate[n]==0):
            turncate_date.append('')
        # 未满16岁的截止日期改为16岁生日当天，判断闰年情况
        elif(birthdate[n] > 20041231):
            if(str(birthdate[n])[4:8] == '0229'):
                years = int(str(birthdate[n])[0:4])+16
                if (not((years % 4 == 0 and years % 100 != 0) or (years % 400 == 0))):
                    turncate_date.append(str(years)+'0301')
                    continue
            turncate_date.append(str(birthdate[n]+160000))
        # 已满16岁但是是72年前的，随机生成2021年到2038年的到期日期，随机生成的日期尾部有“~”号
        elif(birthdate[n] > 19730610 and birthdate[n] <= 20041231):
            random_time = random.randint(time.mktime((
                2021, 1, 1, 0, 0, 0, 0, 0, 0)), time.mktime((2038, 12, 31, 23, 59, 59, 0, 0, 0)))
            turncate_date.append(time.strftime(
                '%Y%m%d', time.localtime(random_time))+'~')
        else:
            turncate_date.append('20991231')
dfo14 = pd.DataFrame({'证件有效截止日期': turncate_date})

# 生成结果表格
writer = pd.ExcelWriter(os.path.dirname(  # pylint: disable=abstract-class-instantiated
    __file__)+'/output.xlsx')
dfo1.to_excel(writer, sheet_name='Sheet1', startcol=0, index=False)
dfo2.to_excel(writer, sheet_name='Sheet1', startcol=1, index=False)
dfo3.to_excel(writer, sheet_name='Sheet1', startcol=2, index=False)
dfo4.to_excel(writer, sheet_name='Sheet1', startcol=3, index=False)
dfo5.to_excel(writer, sheet_name='Sheet1', startcol=4, index=False)
dfo6.to_excel(writer, sheet_name='Sheet1', startcol=5, index=False)
dfo7.to_excel(writer, sheet_name='Sheet1', startcol=6, index=False)
dfo8.to_excel(writer, sheet_name='Sheet1', startcol=7, index=False)
dfo9.to_excel(writer, sheet_name='Sheet1', startcol=8, index=False)
dfo10.to_excel(writer, sheet_name='Sheet1', startcol=9, index=False)
dfo11.to_excel(writer, sheet_name='Sheet1', startcol=10, index=False)
dfo12.to_excel(writer, sheet_name='Sheet1', startcol=11, index=False)
dfo13.to_excel(writer, sheet_name='Sheet1', startcol=12, index=False)
dfo14.to_excel(writer, sheet_name='Sheet1', startcol=13, index=False)
writer.save()
writer.close()
