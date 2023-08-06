# -*- coding: utf-8 -*-
#===========数据分析函数============
#数据分析、统计、报表等相关功能
#许冠明
#20221217
#=======================================

import pandas as pd

def is_float(num):
    """
    判断用户输入的是否为小数或整数
    :param num: str
    :return: bool
    """
    if (num.startswith("-") and num[1:].isdigit()) or num.isdigit():
        return True
    elif num.count(".") == 1 and not num.startswith(".") and not num.endswith("."):
        li = num.split(".")
        if li[0].startswith("-"):
            if li[0][1:].isdigit() and li[1].isdigit():
                return True
            else:
                return False
        else:
            if li[0].isdigit() and li[1].isdigit():
                return True
            else:
                return False
    else:
        return False

def dataCompare(baseData,compareData,IDcol,baseTag='base',compareTag='compare'):
    # 许冠明 20210801
    base=baseData.copy()
    compare=compareData.copy()
    IDcol=IDcol.copy()
    tag1=baseTag
    tag2=compareTag
    columnsTotal=list(base.columns)
    columnsCompare=columnsTotal.copy()
    for i in IDcol:
        columnsCompare.remove(i)
    
    compareC=list(compare.columns)#对比数据的列名
    
    base['_ID']=base[IDcol[0]]
    compare['_ID']=compare[IDcol[0]]
    if len(IDcol)>1:
        
        for i in range(1,len(IDcol)):
            base['_ID']=base['_ID']+' '+base[IDcol[i]]
            compare['_ID']=compare['_ID']+' '+compare[IDcol[i]]

    baseCompareResult=pd.DataFrame(columns=columnsTotal) 
    baseCompareResult['_ID']=base['_ID']
    
    for j in columnsCompare:
        if j in compareC:
            for i in range(base.shape[0]):
                
                baseValue=str(base.loc[i,j])
                if is_float(baseValue):
                    baseValue=str(round(float(base.loc[i,j]),2))
                
                if(len(compare.loc[compare['_ID']== base.loc[i,'_ID'] ,j])>0):
                    compareValue=str(list(compare.loc[compare['_ID']== base.loc[i,'_ID'] ,j])[0])
                    if is_float(compareValue):
                        compareValue=str(round(float(list(compare.loc[compare['_ID']== base.loc[i,'_ID'] ,j])[0]),2))
                        
                    if is_float(baseValue) & is_float(compareValue):
                        if abs(round(float(base.loc[i,j]),2)-round(float(list(compare.loc[compare['_ID']== base.loc[i,'_ID'] ,j])[0]),2))<0.1:
                            #baseCompareResult.loc[i,j]='一致'
                            baseCompareResult.loc[i,j]=base.loc[i,j]
                        else:
                            baseCompareResult.loc[i,j]='不一致，'+tag1+'为'+str(baseValue)+"，"+tag2+"为"+str(compareValue)
                    
                    elif baseValue.replace(' ','')==compareValue.replace(' ',''):
                        #baseCompareResult.loc[i,j]='一致'
                        baseCompareResult.loc[i,j]=base.loc[i,j]
                    elif baseValue in('0.0','nan') and baseValue in('0.0','nan'):
                        #baseCompareResult.loc[i,j]='一致'
                        baseCompareResult.loc[i,j]=base.loc[i,j]
                    
                    else:
                        baseCompareResult.loc[i,j]='不一致，'+tag1+'为'+str(baseValue)+"，"+tag2+"为"+str(compareValue)
                    baseCompareResult.loc[i,'是否有此ID']='匹配成功'
                else:
                    #baseCompareResult.loc[i,j]='Compare没有此行'
                    baseCompareResult.loc[i,j]=base.loc[i,j]
                    baseCompareResult.loc[i,'是否有此ID']=baseTag+'有此ID，但是'+compareTag+'没有此ID'
                if str(baseCompareResult.loc[i,j])=='nan':
                    baseCompareResult.loc[i,j]=''
        else:
                #baseCompareResult[j]='Compare没有此列'  
                print('没有此列')
                print(j+'('+compareTag+'没有此列)')
                baseCompareResult[j]=base[j]
                baseCompareResult=baseCompareResult.rename(columns={j:j+'('+compareTag+'没有此列)'})
                #baseCompareResult.loc[pd.isnull(baseCompareResult[j]),j]=''
        for m in IDcol:
            baseCompareResult[m]=base[m]
        
    #对于在compare数据中，但是不在base中的数据，在id列展示出来
    inCompareNotinBase= pd.DataFrame({'_ID':list(set(compare['_ID']).difference(set(base['_ID']))),'是否有此ID':baseTag+'没有此ID，但'+compareTag+'有此ID'})
    baseCompareResult=baseCompareResult.append(inCompareNotinBase)
        
    return baseCompareResult     


"""
print('对比开始')
path=r'D:\xuguanming\项目信息\04_IT系统项目\202207_XX银行\资金系统\差异对比\imps_accts_invest'
baseData=pd.read_excel(path+'\\旧D层第一部分数据.xlsx',sheet_name='sheet1')
compareData=pd.read_excel(path+'\\新C层数据.xlsx',sheet_name='sheet1')
res=dataCompare(baseData=baseData,compareData=compareData,IDcol=['old_sys_seq'],baseTag='旧数据',compareTag='新数据')
print('对比结束')
"""


