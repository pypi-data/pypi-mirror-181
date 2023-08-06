import pandas as pd
import rdpurchaseorder.operation as db
import rdpurchaseorder.EcsInterface as pe

def classification_process(app2,data):
    '''
    将编码进行去重，然后进行分类
    :param data:
    :return:
    '''

    df=pd.DataFrame(data)

    df.drop_duplicates("FPURORDERNO",keep="first",inplace=True)

    codeList=df['FPURORDERNO'].tolist()

    res=fuz(app2,codeList)

    return res

def fuz(app2,codeList):
    '''
    通过编码分类，将分类好的数据装入列表
    :param app2:
    :param codeList:
    :return:
    '''

    singleList=[]

    for i in codeList:

        data=db.getClassfyData(app2,i)
        singleList.append(data)

    return singleList


def writeSRC(startDate, endDate, app3):
    '''
    将ECS数据取过来插入SRC表中
    :param startDate:
    :param endDate:
    :return:
    '''

    url = "https://kingdee-api.bioyx.cn/dynamic/query"

    page = pe.viewPage(url, 1, 1000, "ge", "le", "v_procurement_order", startDate, endDate, "FPURCHASEDATE")

    for i in range(1, page + 1):
        df = pe.ECS_post_info2(url, i, 1000, "ge", "le", "v_procurement_order", startDate, endDate, "FPURCHASEDATE")

        db.insert_procurement_order(app3, df)

    pass