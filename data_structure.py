#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 15:35:55 2021

@author: zhangmuhan
"""

class property_debt:
    def __init__(self, name, month):
        self.name = name #名称  yes
        self.month = month #月份 yes
        self.asset = True  #yes
        self.attribute = "I" #押品属性 担保融资   yes
        self.expire_structure_shouzhi = [0] * month  #没有0 yes
        self.expire_structure = [0] * month  #有0 yes 如果活期，为0
        self.balance_shouzhi = [0] * month #没有 0
        self.rate_new = [0] * month #新业务利率 yes
        self.balance_base = [0] * (month + 1) #标准期末余额 yes
        self.balance_after = [0] * (month + 1) #优化后期末余额
        self.is_current = True #定期 yes
        self.is_mortgage = True #可抵质押 yes
        self.range_up_spe  = [0] * month  #余额增量的上限 month_size 基于期末余额变动上限设置，在基准净增量为0的时候，用到这个系数
        self.range_low_spe = [0] * month # 余额增量的下限 month_size 基于期末余额变动上限设置 在基准净增量为0的时候，用到这个系数    
        self.asset_type = '其它' #yes
        self.RWA_weight = 0
        self.r1 = 0 #lcr流出系数 yes
        self.r2 = 0 #lcr折算系数 yes
        self.r3 = [] #押品比例系数 yes