#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 17:29:05 2021

@author: zhangmuhan
"""

from scipy.optimize import minimize
import data_input as dp



#month: 1- 13
def run(month):
    RWA_Kr = 1.05
    net = dp.net
    total_month = 13  #这里之后要改！！！用于计算NII

    #total: 当月负债和资产的base总和
    #total_before:上月负债和资产的base的总和
    #after:当月负债和资产的优化总和
    #after_before：上月负债和资产的优化总和
    total = []
    total_before = []
    after_before = []    
    
    for i in range(len(net)):
        total.append(dp.net[i].balance_base[month])
        total_before.append(dp.net[i].balance_base[month - 1])


    if month == 1:
        after_before = total_before
    else:
        for i in range(len(net)):
            after_before.append(dp.net[i].balance_after[month - 1])

    
    expire_structure = []
    for i in range(len(net)): 
        expire_structure.append(dp.net[i].expire_structure_shouzhi[month - 1])
    
    


    
    #优化前后资产总增量相等
    #equal
    def total_increment_capital(after): #after
        sum1 = 0
        sum2 = 0
        for i in range(len(net)):
            if net[i].asset == True:
                sum1 += total[i] - total_before[i]
                sum2 += after[i] - after_before[i]
        return sum1 - sum2
    #equal
    def total_increment_debt(after): #after
        sum1 = 0
        sum2 = 0
        for i in range(len(net)):
            if net[i].asset == False:
                sum1 += total[i] - total_before[i]
                sum2 += after[i] - after_before[i]
        return sum1 - sum2
    

    def rwa(after):
        sum1 = 0
        sum2 = 0
        for i in range(len(net)):
            if net[i].asset == True:
                sum1 += (total[i] - total_before[i] + net[i].expire_structure[month - 1]) * net[i].RWA_weight
                sum2 += (after[i] - after_before[i] + net[i].expire_structure[month - 1]) * net[i].RWA_weight
        return -(sum2 / sum1) + RWA_Kr
    
    '''
    def lcr(after):
        lcr_result = dp.lcr_setup(month)
        r1 = lcr_result[0]
        r2 = lcr_result[1]
        r3 = lcr_result[2]
        r4 = lcr_result[3]
        A = lcr_result[4]
        B = lcr_result[5]
        C = lcr_result[6]
        P = lcr_result[7]
        L = lcr_result[8]
        
        KMAP = 0
        KMA = 0
        
        al = dp.p_all + dp.d_all
        for i in range(len(after)):
            if al[i].is_mortgage == 'y':
                KMA += total[i] - total_before[i]    
                KMAP += after[i] - after_before[i] 
                
        A1 = r3[3 - 1] + r3[6 - 1] - r3[14 - 1] + r3[13 - 1] + r3[15 - 1] + r3[17 - 1] - r3[1 - 1] - r3[5 - 1] - r3[7 - 1] - r3[9 - 1] - r3[11 - 1] 
        A2 = r3[3 - 1] + r3[8 - 1] - r3[16 - 1] 
        A3 = r3[4 - 1] + r3[10 - 1] + r3[12 - 1] - r3[18 - 1]
    
        C11 = 0
        for i in range(len(A)):
            C11 += A[i] * r1[i] * r2[i]
        C11 += r4[1 - 1]
        C11 = C11 - (KMAP - KMA)


        C12 = 0
        for i in range(len(B)):
            C12 += B[i] * r1[i] * r2[i]
  
        C13 = 0
        for i in range(len(C)):
            C13 += C[i] * r1[i] * r2[i]

        C21 = 0 
        for i in range(len(L)):
            C21 += L[i] * r1[i + cut] * r2[i + cut]        
        C21 += r4[2 - 1] + r4[3 - 1] + r4[4 - 1]



        C22 = 0
        for i in range(len(P)):
            C22 += P[i] * r1[i] * r2[i]
        C22 += r4[5 - 1] + r4[6 - 1]

    
        A11 = max(A1 + C11, 0)
        A21 = A2 + C12
        A31 = A3 + C13
        A32 = max(A31 - 15/85*(A11 + A21), A31 - 15/60*A11, 0)
        A4 = max(A21 + A31 - A32 - 2/3*A11, 0)
    
        C1 = C11 + C12 + C13 - A32 - A4
        C2 = C21 - min(C22, 0.75 * C21)
        return 1.02 - C1 / C2
    '''
    
    
    #print(lcr(total))
    
    #所有资产和负债都需大于0
    def find_bound():
        bound = []
        for i in range(len(net)):
            up = max(total[i] * (net[i].range_low_spe[month - 1] + 1), total[i] * (net[i].range_up_spe[month - 1]+ 1))
            low = min(total[i] * (net[i].range_low_spe[month - 1] + 1), total[i] * (net[i].range_up_spe[month - 1] + 1))   
            low = max(low, 0)
            bound.append((low, up))
        return bound

    bound = find_bound()  #loower and upper bound for all assets included

    

    

    def NII(after):
        temp = 0
        a1_total = 0
        a2_total = 0

        for i in range(len(net)):
            if net[i].asset == True:
                if net[i].is_current:
                    a1_total += (after[i] - after_before[i] + net[i].expire_structure[month - 1]) * net[i].rate_new[month - 1]
                else:
                    temp1 = 0
                    temp2 = after[i] - after_before[i] + net[i].expire_structure[month - 1]
                    sigma = 0.5 * net[i].rate_new[month - 1]
                    for j in range(month, total_month):
                        sigma += net[i].rate_new[j - 1]
                    temp1 = temp2 * sigma
                    a2_total += temp1
            else:
                if net[i].is_current:
                    temp += (after[i] - after_before[i] + net[i].expire_structure[month - 1]) * net[i].rate_new[month - 1]
                    a1_total -= (after[i] - after_before[i] + net[i].expire_structure[month - 1]) * net[i].rate_new[month - 1]
                else:
                    temp1 = 0
                    temp2 = after[i] - after_before[i] + net[i].expire_structure[month - 1]
                    sigma = 0.5 * net[i].rate_new[month - 1]
                    for j in range(month, total_month):
                        sigma += net[i].rate_new[j - 1]
                    temp1 = temp2 * sigma
                    a2_total -= temp1
        a2_total = a2_total / 1200
        a1_total = a1_total * (total_month + 1 - month - 0.5) / 1200  #这里total month要改！

        b1_total = 0
        b2_total = 0
        for i in range(len(net)):
            if net[i].asset == True:
                if net[i].is_current:
                    b1_total += expire_structure[i] * net[i].balance_shouzhi[month - 1]
                else:
                    b2_total += expire_structure[i] * net[i].balance_shouzhi[month - 1] / 1200
            else:
                if net[i].is_current:
                    b1_total -= expire_structure[i] * net[i].balance_shouzhi[month - 1]
                else:
                    b2_total -= expire_structure[i] * net[i].balance_shouzhi[month - 1] / 1200
        b1_total = b1_total * (month - 0.5) / 1200

        return (a1_total + a2_total + b1_total + b2_total) * -1 #因为之后函数只能找minimum，所以要乘-1来找maximum
    

    

    cons = []
    cons.append({'type': 'eq', 'fun': total_increment_capital})
    cons.append({'type': 'eq', 'fun': total_increment_debt})
    cons.append({'type': 'ineq', 'fun': rwa})
    #cons.append({'type': 'ineq', 'fun': lcr})
    



    #SLSQP
    res = minimize(NII, total, method = 'trust-constr', bounds = bound, constraints = cons)
    for i in range(len(net)):
        net[i].balance_after[month] = res.x[i]
        
    return res.x, res.fun

for i in range(1, 14):
    result = run(i)
    print(result[1])
    

 