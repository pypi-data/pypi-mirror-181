def getCode(app3):
    '''
    查询出表中的编码
    :param app2:
    :return:
    '''

    sql="select FBillNo,Fseq,Fdate,FDeptName,FItemNumber,FItemName,FItemModel,FUnitName,Fqty,FStockName,Flot,Fnote,FPRODUCEDATE,FEFFECTIVEDATE,FSUMSUPPLIERLOT,FAFFAIRTYPE,FIsdo from RDS_ECS_ODS_DISASS_DELIVERY where FIsdo=0"

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

def iskfperiod(app2,FNumber):
    '''
    查看物料是否启用保质期
    :param app2:
    :param FNumber:
    :return:
    '''

    sql=f"select FISKFPERIOD from rds_vw_fiskfperiod where F_SZSP_SKUNUMBER='{FNumber}'"

    res=app2.select(sql)

    if res==[]:

        return ""

    else:

        return res[0]['FISKFPERIOD']


def getSubEntityCode(app2,FNumber):
    '''
    获得子件信息
    :return:
    '''

    sql=f"select * from RDS_ECS_ODS_ASS_STORAGEACCT where FBillNo='{FNumber}'"

    res=app2.select(sql)

    return res

def changeStatus(app3,fnumber,status):
    '''
    将没有写入的数据状态改为2
    :param app2: 执行sql语句对象
    :param fnumber: 订单编码
    :param status: 数据状态
    :return:
    '''

    sql=f"update a set a.FIsdo={status} from RDS_ECS_ODS_DISASS_DELIVERY a where FBillNo='{fnumber}'"

    app3.update(sql)

def checkDataExist(app2, tableName,FBillNo):
    '''
    通过FSEQ字段判断数据是否在表中存在
    :param app2:
    :param FSEQ:
    :return:
    '''
    sql = f"select FBillNo from {tableName} where FBillNo='{FBillNo}'"

    res = app2.select(sql)

    if res == []:

        return True

    else:

        return False


def getFinterId(app2,tableName):
    '''
    在两张表中找到最后一列数据的索引值
    :param app2: sql语句执行对象
    :param tableName: 要查询数据对应的表名表名
    :return:
    '''

    sql = f"select isnull(max(FInterId),0) as FMaxId from {tableName}"

    res = app2.select(sql)

    return res[0]['FMaxId']

def insert_assembly_order(app2,data):
    '''
    组装单
    :param app2:
    :param data:
    :return:
    '''

    for i in data.index:

        if checkDataExist(app2,"RDS_ECS_SRC_ASS_STORAGEACCT",data.iloc[i]['FBillNo']):

            sql = f"insert into RDS_ECS_SRC_ASS_STORAGEACCT(FInterID,FBillNo,Fseq,Fdate,FDeptName,FItemNumber,FItemName,FItemModel,FUnitName,Fqty,FStockName,Flot,FBomNumber,FNote,FPRODUCEDATE,FEFFECTIVEDATE,FSUMSUPPLIERLOT,FAFFAIRTYPE) values({getFinterId(app2,'RDS_ECS_SRC_ASS_STORAGEACCT')+1},'{data.iloc[i]['FBillNo']}','{data.iloc[i]['Fseq']}','{data.iloc[i]['Fdate']}','{data.iloc[i]['FDeptName']}','{data.iloc[i]['FItemNumber']}','{data.iloc[i]['FItemName']}','{data.iloc[i]['FItemModel']}','{data.iloc[i]['FUnitName']}','{data.iloc[i]['Fqty']}','{data.iloc[i]['FStockName']}','{data.iloc[i]['Flot']}','{data.iloc[i]['FBomNumber']}','{data.iloc[i]['Fnote']}','{data.iloc[i]['FPRODUCEDATE']}','{data.iloc[i]['FEFFECTIVEDATE']}','{data.iloc[i]['FSUMSUPPLIERLOT']}','{data.iloc[i]['FAFFAIRTYPE']}')"

            app2.insert(sql)


def insert_remove_order(app2,data):
    '''
    拆卸单
    :param app2:
    :param data:
    :return:
    '''

    for i in data.index:

        if checkDataExist(app2,"RDS_ECS_SRC_DISASS_DELIVERY",data.iloc[i]['FBillNo']):

            sql = f"insert into RDS_ECS_SRC_DISASS_DELIVERY(FInterID,FBillNo,Fseq,Fdate,FDeptName,FItemNumber,FItemName,FItemModel,FUnitName,Fqty,FStockName,Flot,FNote,FPRODUCEDATE,FEFFECTIVEDATE,FSUMSUPPLIERLOT,FAFFAIRTYPE) values({getFinterId(app2,'RDS_ECS_SRC_DISASS_DELIVERY')+1},'{data.iloc[i]['FBillNo']}','{data.iloc[i]['Fseq']}','{data.iloc[i]['Fdate']}','{data.iloc[i]['FDeptName']}','{data.iloc[i]['FItemNumber']}','{data.iloc[i]['FItemName']}','{data.iloc[i]['FItemModel']}','{data.iloc[i]['FUnitName']}','{data.iloc[i]['Fqty']}','{data.iloc[i]['FStockName']}','{data.iloc[i]['Flot']}','{data.iloc[i]['Fnote']}','{data.iloc[i]['FPRODUCEDATE']}','{data.iloc[i]['FEFFECTIVEDATE']}','{data.iloc[i]['FSUMSUPPLIERLOT']}','{data.iloc[i]['FAFFAIRTYPE']}')"

            app2.insert(sql)