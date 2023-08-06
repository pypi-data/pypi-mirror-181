import pandas as pd

def getCode(app3):
    '''
    查询出表中的编码
    :param app2:
    :return:
    '''

    sql="select FPURORDERNO from RDS_ECS_ODS_pur_poorder where FIsdo=0 and FIsFree!=1"

    res=app3.select(sql)

    return res

def getClassfyData(app3,code):
    '''
    获得分类数据
    :param app2:
    :param code:
    :return:
    '''

    sql=f"select FPURORDERNO,FBILLTYPENAME,FPURCHASEDATE,FCUSTOMERNUMBER,FSUPPLIERNAME,FPOORDERSEQ,FPRDNUMBER,FPRDNAME,FQTY,FPRICE,FAMOUNT,FTAXRATE,FTAXAMOUNT,FTAXPRICE,FORAMOUNTFALL,FPURCHASEDEPTID,FPURCHASEGROUPID,FPURCHASERID,FDESCRIPTION,FUploadDate,FIsDo,FDeliveryDate,FIsFree from RDS_ECS_ODS_pur_poorder where FPURORDERNO='{code}'"

    res=app3.select(sql)

    return res

def code_conversion(app2,tableName,param,param2):
    '''
    通过ECS物料编码来查询系统内的编码
    :param app2: 数据库操作对象
    :param tableName: 表名
    :param param:  参数1
    :param param2: 参数2
    :return:
    '''

    sql=f"select FNumber from {tableName} where {param}='{param2}'"

    res=app2.select(sql)

    if res==[]:

        return ""

    else:

        return res[0]['FNumber']

def code_conversion_org(app2,tableName,param,param2,param3):
    '''
    通过ECS物料编码来查询系统内的编码
    :param app2: 数据库操作对象
    :param tableName: 表名
    :param param:  参数1
    :param param2: 参数2
    :return:
    '''

    sql=f"select FNumber from {tableName} where {param}='{param2}' and FORGNUMBER='{param3}'"

    res=app2.select(sql)

    if res==[]:

        return ""

    else:

        return res[0]['FNumber']

def changeStatus(app2,fnumber,status):
    '''
    将没有写入的数据状态改为2
    :param app2: 执行sql语句对象
    :param fnumber: 订单编码
    :param status: 数据状态
    :return:
    '''

    sql=f"update a set a.FIsDo={status} from RDS_ECS_ODS_pur_poorder a where FPURORDERNO='{fnumber}'"

    app2.update(sql)


def checkDataExist(app2, FOrderId):
    '''
    通过FSEQ字段判断数据是否在表中存在
    :param app2:
    :param FSEQ:
    :return:
    '''
    sql = f"select FOrderId from RDS_ECS_SRC_pur_poorder where FOrderId='{FOrderId}'"

    res = app2.select(sql)

    if res == []:

        return True

    else:

        return False


def insert_procurement_order(app2,data):
    '''
    采购订单
    :param app2:
    :param data:
    :return:
    '''

    for i in data.index:

        if checkDataExist(app2,data.iloc[i]['FOrderId']):

            sql = f"insert into RDS_ECS_SRC_pur_poorder(FPURORDERNO,FBILLTYPENAME,FPURCHASEDATE,FCUSTOMERNUMBER,FSUPPLIERNAME,FPOORDERSEQ,FPRDNUMBER,FPRDNAME,FQTY,FPRICE,FAMOUNT,FTAXRATE,FTAXAMOUNT,FTAXPRICE,FORAMOUNTFALL,FPURCHASEDEPTID,FPURCHASEGROUPID,FPURCHASERID,FUploadDate,FIsDo,FIsFree,FUpDateTime,FOrderId) values('{data.iloc[i]['FPURORDERNO']}','{data.iloc[i]['FBILLTYPENAME']}','{data.iloc[i]['FPURCHASEDATE']}','{data.iloc[i]['FCUSTOMERNUMBER']}','{data.iloc[i]['FSUPPLIERNAME']}','{data.iloc[i]['FPOORDERSEQ']}','{data.iloc[i]['FPRDNUMBER']}','{data.iloc[i]['FPRDNAME']}','{data.iloc[i]['FQTY']}','{data.iloc[i]['FPRICE']}','{data.iloc[i]['FAMOUNT']}','{data.iloc[i]['FTAXRATE']}','{data.iloc[i]['FTAXAMOUNT']}','{data.iloc[i]['FTAXPRICE']}','{data.iloc[i]['FAMOUNT']}','{data.iloc[i]['FPURCHASEDEPTID']}','{data.iloc[i]['FPURCHASEGROUPID']}','{data.iloc[i]['FPURCHASERID']}',getdate(),0,0,getdate(),'{data.iloc[i]['FOrderId']}')"

            app2.insert(sql)