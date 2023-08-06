def getCode(app3):
    '''
    查询出表中的编码
    :param app2:
    :return:
    '''

    sql="select FGODOWNNO from RDS_ECS_ODS_pur_storageacct where FIsdo=0 and FIsFree!=1"

    res=app3.select(sql)

    return res

def getClassfyData(app3,code):
    '''
    获得分类数据
    :param app2:
    :param code:
    :return:
    '''

    sql=f"select * from RDS_ECS_ODS_pur_storageacct where FGODOWNNO='{code}'"

    res=app3.select(sql)

    return res

def changeStatus(app3,fnumber,status):
    '''
    将没有写入的数据状态改为2
    :param app2: 执行sql语句对象
    :param fnumber: 订单编码
    :param status: 数据状态
    :return:
    '''

    sql=f"update a set a.FIsdo={status} from RDS_ECS_ODS_pur_storageacct a where FGODOWNNO='{fnumber}'"

    app3.update(sql)


def checkDataExist(app2, FInstockId):
    '''
    通过FSEQ字段判断数据是否在表中存在
    :param app2:
    :param FSEQ:
    :return:
    '''
    sql = f"select FInstockId from RDS_ECS_SRC_pur_storageacct where FInstockId='{FInstockId}'"

    res = app2.select(sql)

    if res == []:

        return True

    else:

        return False


def insert_procurement_storage(app2,data):
    '''
    采购入库
    :param app2:
    :param data:
    :return:
    '''

    for i in data.index:

        if checkDataExist(app2,data.iloc[i]['FInstockId']):

            sql=f"insert into RDS_ECS_SRC_pur_storageacct(FGODOWNNO,FBILLNO,FPOORDERSEQ,FBILLTYPEID,FDOCUMENTSTATUS,FSUPPLIERFIELD,FCUSTOMERNUMBER,FSUPPLIERNAME,FSUPPLIERABBR,FSTOCKID,FLIBRARYSIGN,FBUSINESSDATE,FBARCODE,FGOODSID,FPRDNAME,FINSTOCKQTY,FPURCHASEPRICE,FAMOUNT,FTAXRATE,FLOT,FCHECKSTATUS,FDESCRIPTION,FUPDATETIME,FInstockId) values('{data.iloc[i]['FGODOWNNO']}','{data.iloc[i]['FBILLNO']}','{data.iloc[i]['FPOORDERSEQ']}','{data.iloc[i]['FBILLTYPEID']}','{data.iloc[i]['FDOCUMENTSTATUS']}','{data.iloc[i]['FSUPPLIERFIELD']}','{data.iloc[i]['FCUSTOMERNUMBER']}','{data.iloc[i]['FSUPPLIERNAME']}','{data.iloc[i]['FSUPPLIERABBR']}','{data.iloc[i]['FSTOCKID']}','{data.iloc[i]['FLIBRARYSIGN']}','{data.iloc[i]['FBUSINESSDATE']}','{data.iloc[i]['FBARCODE']}','{data.iloc[i]['FGOODSID']}','{data.iloc[i]['FPRDNAME']}','{data.iloc[i]['FINSTOCKQTY']}','{data.iloc[i]['FPURCHASEPRICE']}','{data.iloc[i]['FAMOUNT']}','{data.iloc[i]['FTAXRATE']}','{data.iloc[i]['FLOT']}','{data.iloc[i]['FCHECKSTATUS']}','',getdate(),{data.iloc[i]['FInstockId']})"

            app2.insert(sql)
