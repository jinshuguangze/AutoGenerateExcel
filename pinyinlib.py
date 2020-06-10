# -*- coding: utf-8 -*-
import os
import xpinyin
class Pinyin(object):
    dataName_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'name_dict.dat')
    def __init__(self,dataName_path=dataName_path):
        self.dictName = {}
        with open(dataName_path,encoding='UTF-8') as f:#注意编码问题
            for line in f:
                key,val = line.split('=')
                self.dictName[key]=val
        f.close()

    #判断是否是姓氏，是返回
    def convert_name(self,chars=u''):
        if(chars == ''):
            return -1
        try:
            return self.dictName[chars]
        except:
            return -1

    #获取姓名拼音
    #convert支持capitalize、lower、upper三种 tone_marks 支持marks（声调）、numbers（数字声调）
    def get_pinyin_name(self,chars=u'王大锤',splitter=u'-',tone_marks=None,convert='lower'):
        result = []
        nameLen = 0
        if self.convert_name(chars[:2]) != -1:
            result=result+self.convert_name(chars[:2]). strip().split(u'-')#strip()，清除两边空白字符
            nameLen=2
        elif self.convert_name(chars[:1]) != -1:
            result.append(self.convert_name(chars[:1]). strip())
            nameLen = 1
        result = result+(xpinyin.Pinyin().get_pinyin(chars[nameLen:],u'-','numbers','lower').split(u'-'))#先取数字声调，再出处理
        for i in range(len(result)):# for char in result 不能修改值
            if tone_marks == 'marks':
                result[i] = xpinyin.Pinyin().decode_pinyin(result[i])
            elif tone_marks == 'numbers':
                pass
            else:
                result[i] = result[i] [:-1]#去除数字
                result[i] = xpinyin.Pinyin().convert_pinyin(result[i] ,convert)
        return splitter.join(result)
