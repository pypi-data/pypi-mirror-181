import rdpurchaseorder.operation as pro
import json
def json_model(app2,model_data):

    '''
    物料单元model
    :param model_data: 物料信息
    :return:
    '''

    if pro.code_conversion_org(app2,"rds_vw_material","F_SZSP_SKUNUMBER",str(model_data['FPRDNUMBER']),"104"):

        model={

            "FProductType": "1",
            "FMaterialId": {
                "FNumber": "7.1.000001" if str(model_data['FPRDNUMBER'])=='1' else pro.code_conversion_org(app2,"rds_vw_material","F_SZSP_SKUNUMBER",str(model_data['FPRDNUMBER']),"104")
            },
            "FMaterialDesc": str(model_data['FPRDNAME']),
            # "FUnitId": {
            #     "FNumber": "01"
            # },
            "FQty": str(model_data['FQTY']),
            # "FPriceUnitId": {
            #     "FNumber": "01"
            # },
            "FPriceUnitQty": str(model_data['FQTY']),
            "FPriceBaseQty": str(model_data['FQTY']),
            "FDeliveryDate": str(model_data['FDeliveryDate']),
            "FPrice": str(model_data['FPRICE']),
            "FTaxPrice": str(model_data['FTAXPRICE']),
            "FEntryTaxRate": float(model_data['FTAXRATE'])*100,
            "FRequireOrgId": {
                "FNumber": "104"
            },
            "FReceiveOrgId": {
                "FNumber": "104"
            },
            "FEntrySettleOrgId": {
                "FNumber": "104"
            },
            "FGiveAway": True if model_data['FIsFree']==1 else False,
            "FEntryNote": str(model_data['FDESCRIPTION']),
            # "FStockUnitID": {
            #     "FNumber": "01"
            # },
            "FStockQty": str(model_data['FQTY']),
            "FStockBaseQty": str(model_data['FQTY']),
            "FDeliveryControl": True,
            "FTimeControl": False,
            "FDeliveryMaxQty": str(model_data['FQTY']),
            "FDeliveryMinQty": str(model_data['FQTY']),
            "FDeliveryEarlyDate": str(model_data['FDeliveryDate']),
            "FDeliveryLastDate": str(model_data['FDeliveryDate']),
            "FPriceCoefficient": 1.0,
            "FEntrySettleModeId": {
                "FNumber": "JSFS04_SYS"
            },
            "FPlanConfirm": True,
            # "FSalUnitID": {
            #     "FNumber": "01"
            # },
            "FSalQty": str(model_data['FQTY']),
            "FCentSettleOrgId": {
                "FNumber": "104"
            },
            "FDispSettleOrgId": {
                "FNumber": "104"
            },
            "FDeliveryStockStatus": {
                "FNumber": "KCZT02_SYS"
            },
            "FIsStock": False,
            "FSalBaseQty": str(model_data['FQTY']),
            "FEntryPayOrgId": {
                "FNumber": "104"
            },
            # "FAllAmountExceptDisCount": 54520.0,
            "FEntryDeliveryPlan": [
                {
                    "FDeliveryDate_Plan": str(model_data['FDeliveryDate']),
                    "FPlanQty": str(model_data['FQTY']),
                    "FPREARRIVALDATE": str(model_data['FDeliveryDate'])
                }
            ]
        }

        return model
    else:
        return []


def data_splicing(app2,data):
    '''
    将订单内的物料进行遍历组成一个列表，然后将结果返回给 FPOOrderEntry
    :param data:
    :return:
    '''
    list=[]

    for i in data:

        if json_model(app2,i):

            list.append(json_model(app2,i))

        else:

            return []

    return list


def ERP_Save(api_sdk,data,option,app2,app3):
    '''
        调用ERP保存接口
        :param api_sdk: 调用ERP对象
        :param data:  要插入的数据
        :param option: ERP密钥
        :param app2: 数据库执行对象
        :return:
        '''

    erro_list = []
    sucess_num = 0
    erro_num = 0

    api_sdk.InitConfig(option['acct_id'], option['user_name'], option['app_id'],
                       option['app_sec'], option['server_url'])

    for i in data:

        if check_order_exists(api_sdk,str(i[0]['FPURORDERNO']))!=True:

                model={
                        "Model": {
                            "FID": 0,
                            "FBillTypeID": {
                                "FNUMBER": "CGDD01_SYS"
                            },
                            "FBillNo": str(i[0]['FPURORDERNO']),
                            "FDate": str(i[0]['FPURCHASEDATE']),
                            "FSupplierId": {
                                "FNumber": pro.code_conversion_org(app2,"rds_vw_supplier","FNAME",i[0]['FSUPPLIERNAME'],"104")
                            },
                            "FPurchaseOrgId": {
                                "FNumber": "104"
                            },
                            "FPurchaseDeptId": {
                                "FNumber": "BM000040"
                            },
                            "FPurchaserGroupId": {
                                "FNumber": "SKYX02"
                            },
                            "FPurchaserId": {
                                "FNumber": pro.code_conversion(app2,"rds_vw_buyer","FNAME",str(i[0]['FPURCHASERID']))
                            },
                            "FProviderId": {
                                "FNumber": pro.code_conversion_org(app2,"rds_vw_supplier","FNAME",i[0]['FSUPPLIERNAME'],"104")
                            },
                            "FSettleId": {
                                "FNumber": pro.code_conversion_org(app2,"rds_vw_supplier","FNAME",i[0]['FSUPPLIERNAME'],"104")
                            },
                            "FChargeId": {
                                "FNumber": pro.code_conversion_org(app2,"rds_vw_supplier","FNAME",i[0]['FSUPPLIERNAME'],"104")
                            },
                            "FCorrespondOrgId": {
                                "FNumber": pro.code_conversion_org(app2,"rds_vw_supplier","FNAME",i[0]['FSUPPLIERNAME'],"104")
                            },
                            "FIsModificationOperator": False,
                            "FChangeStatus": "A",
                            "FACCTYPE": "Q",
                            "F_SZSP_CGLX": {
                                "FNumber": "LX07"
                            },
                            "F_SZSP_SHR": {
                                "FSTAFFNUMBER": "BSP00040"
                            },
                            "FIsMobBill": False,
                            "FIsUseDrpSalePOPush": False,
                            "F_SZSP_ReceCloseFlag": False,
                            "F_SZSP_FPCloseFlag": False,
                            "F_SZSP_PayCloseFlag": False,
                            "F_SZSP_initComfirmation": False,
                            "FPOOrderFinance": {
                                "FSettleModeId": {
                                    "FNumber": "JSFS04_SYS"
                                },
                                "FPayConditionId": {
                                    "FNumber": "003"
                                },
                                "FSettleCurrId": {
                                    "FNumber": "PRE001"
                                },
                                "FExchangeTypeId": {
                                    "FNumber": "HLTX01_SYS"
                                },
                                "FExchangeRate": 1.0,
                                "FPriceTimePoint": "1",
                                "FFOCUSSETTLEORGID": {
                                    "FNumber": "104"
                                },
                                "FIsIncludedTax": True,
                                "FISPRICEEXCLUDETAX": True,
                                "FLocalCurrId": {
                                    "FNumber": "PRE001"
                                },
                                "FSupToOderExchangeBusRate": 1.0,
                                "FSEPSETTLE": False
                            },
                            "FPOOrderEntry": data_splicing(app2,i)
                        }
                    }

                result=json.loads(api_sdk.Save("PUR_PurchaseOrder",model))

                if result['Result']['ResponseStatus']['IsSuccess']:

                    res_submit=ERP_Submit(api_sdk,str(i[0]['FPURORDERNO']))

                    if res_submit:

                        res_audit=ERP_Audit(api_sdk,str(i[0]['FPURORDERNO']))

                        if res_audit:

                            pro.changeStatus(app3, str(i[0]['FPURORDERNO']), "1")
                            sucess_num=sucess_num+1

                            pass

                    else:

                        pro.changeStatus(app3, str(i[0]['FPURORDERNO']), "2")
                        pass

                else:
                    pro.changeStatus(app3,str(i[0]['FPURORDERNO']),"2")

                    erro_num=erro_num+1
                    erro_list.append(result)


    dict = {
        "sucessNum": sucess_num,
        "erroNum": erro_num,
        "erroList": erro_list
    }

    return dict


def check_order_exists(api_sdk,FNumber):
    '''
    查看订单是否在ERP系统存在
    :param api: API接口对象
    :param FNumber: 订单编码
    :return:
    '''

    model={
            "CreateOrgId": 0,
            "Number": FNumber,
            "Id": "",
            "IsSortBySeq": "false"
        }

    res=json.loads(api_sdk.View("PUR_PurchaseOrder",model))

    return res['Result']['ResponseStatus']['IsSuccess']

def ERP_Submit(api_sdk,FNumber):
    '''
    将订单进行提交
    :param api_sdk: API接口对象
    :param FNumber: 订单编码
    :return:
    '''

    model={
        "CreateOrgId": 0,
        "Numbers": [FNumber],
        "Ids": "",
        "SelectedPostId": 0,
        "NetworkCtrl": "",
        "IgnoreInterationFlag": ""
    }

    res=json.loads(api_sdk.Submit("PUR_PurchaseOrder",model))

    return res['Result']['ResponseStatus']['IsSuccess']

def ERP_Audit(api_sdk,FNumber):
    '''
    将订单审核
    :param api_sdk: API接口对象
    :param FNumber: 订单编码
    :return:
    '''

    model={
        "CreateOrgId": 0,
        "Numbers": [FNumber],
        "Ids": "",
        "InterationFlags": "",
        "NetworkCtrl": "",
        "IsVerifyProcInst": "",
        "IgnoreInterationFlag": ""
    }

    res = json.loads(api_sdk.Audit("PUR_PurchaseOrder", model))

    return res['Result']['ResponseStatus']['IsSuccess']



