#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 15:33:46 2021

@author: zhangmuhan
"""
import xlrd
from data_structure import property_debt

def run(data_in_file): 
    net = [] #everything except partial bits of LCR
    month_size = 13
    ExcelFile=xlrd.open_workbook(data_in_file)
    
    sheet1 = ExcelFile.sheet_by_name('基准期末余额')
    sheet2 = ExcelFile.sheet_by_name('属性')
    sheet3 = ExcelFile.sheet_by_name('存量到期结构')
    sheet4 = ExcelFile.sheet_by_name('押品比例系数')
    sheet5 = ExcelFile.sheet_by_name('LCR参数')
    sheet6 = ExcelFile.sheet_by_name('新增业务利率')
    sheet7 = ExcelFile.sheet_by_name('RWA系数')
    sheet8 = ExcelFile.sheet_by_name('上限')
    sheet9 = ExcelFile.sheet_by_name('下限')
    
    for row in range(1, 10):
        if row == 5 or row == 6:
            continue 

        new = property_debt(sheet1.cell(row, 0).value, month_size) #name
        
        if sheet2.cell(row, 1).value == 'A':#asset
            new.asset = True
        else:
            new.asset = False
        
        new.attribute = sheet2.cell(row, 2).value #attribute
        new.asset_type = sheet2.cell(row, 3).value #asset_type

        if sheet2.cell(row, 4).value == "N":        #is_mortgage
            new.is_mortgage = False
        else:
            new.is_mortgage = True
            
        if sheet2.cell(row, 5).value =="定期":        #定期活期 is_current
            new.is_current = True
        else:
            new.is_current = False
        

        if new.attribute != 'D': #r3
            new.r3.append(sheet4.cell(row, 1).value)
        else:
            for i in range(1, 5):
                new.r3.append(sheet4.cell(row, i).value)
        
        new.r1 = sheet5.cell(row, 1).value #r1
        new.r2 = sheet5.cell(row, 3).value #r2
        
        if new.asset == True: #资产项目 rwa系数
            new.RWA_weight = sheet7.cell(row, 1).value
        
        
        for column in range(1, 15):
            new.balance_base[column - 1] = sheet1.cell(row, column).value        #balance_Base
            if column != 14:
                new.expire_structure[column - 1] = sheet3.cell(row, column).value    #存量到期结构
                
                if new.is_current == True: #balance_shouzhi
                    new.balance_shouzhi[column - 1] = new.expire_structure[column - 1]
                else:
                    new.balance_shouzhi[column - 1] = new.balance_base[0]
                    
                new.rate_new[column - 1] = sheet6.cell(row, column).value   #新业务利率
                new.range_up_spe[column - 1] = sheet8.cell(row, column).value     #上限
                new.range_low_spe[column - 1] = sheet9.cell(row, column).value     #下限
        
        net.append(new)
        
    return net
            
            

net = run("/Users/zhangmuhan/Desktop/实习/My_code/Second/7项产品测试 2.xlsx")


        
    