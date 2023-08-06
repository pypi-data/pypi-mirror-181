import copy
import re

debugEnable = False
icmFlag = "HOST_"
aeroFlag = "HOST_AERO_"

class ApiDataBean:
    def __init__(self):
        """
        存储了每个API的所有信息
        存储在RowDataBean的api中来保持对应关系
        returnType:返回值类型,
        dataType:数据类型,针对set类型的API新增的
        """
        self.index = 0
        self.apiName = ""
        self.funcName = ""
        self.jniName = ""
        self.apiDesc = ""
        self.unit = ""
        self.paramsDesc = ""
        self.signal = ""
        self.returnType = ""
        self.dataType = ""
        self.permission = ""


class RowDataBean:
    def __init__(self):
        """
        每一个API及prop对应的关系
        以API为主,如果是数组:每一个API对应多个信息
        apitype:set还是get
        isArray:是否是数组
        apiList:数组api,会存在多个api列表,每一个数据表示不同的数据
        parentPropCdu:prop的父prop
        prop:为空说明是子prop,父类为parentPropCdu
        permission:存储了该prop所有权限
        setSignal:存储了所有的set信号
        """
        self.users = ""
        self.apiType = ""
        self.apiList = []
        self.apiCount = 0
        self.callback = ""
        self.parentCallback = ""
        self.prop = ""
        self.parentPropCdu = ""
        self.parentPropIcm = ""
        self.parentPropAero = ""
        self.permission = []
        self.setSignal = []
        self.isArray = False
        self.genCarApi = True


def findLastProp(rowDataBeanList):
    """
    查找最后一个prop父类
    :param rowDataBeanList:已有的行数据集
    :return:
    """
    for rowDataBean in reversed(rowDataBeanList):
        if rowDataBean.prop != "":
            return rowDataBean
    # 方便调试
    return RowDataBean()


def parseRowData(rowDataList):
    """
    解析每一行数据，将其分类，将数组解析出来
    :param rowDataList:
    :return:
    """
    rowDataBeanList = []
    for rowData in rowDataList:
        users = rowData["有效性"]
        if users is None or users.value == '':
            continue
        apiType = rowData["API类型"]
        api = rowData["API"]
        apiDesc = rowData["功能说明"]
        paramsDesc = rowData["参数说明"]
        unit = rowData["单位"]
        callback = rowData["Callback"]
        prop = rowData["Prop"]
        permission = rowData["权限"]
        setSignal = rowData["Signal"]
        jniApi = rowData["JNI"]
        genCarApi = rowData["GenCarApi"]
        #trans = rowData["Trans"]

        # 数组类型，第二行api名称为空
        if api is not None and api.value != "":
            # int int[] int[12]
            returnTypePatter = '(?P<returnType>\w+|\w+\[\d+\]|\w+\[\d?\])'

            result = re.search(returnTypePatter+"\s(?P<funcName>\w+)", api.value)
            apiReturnType = result.group("returnType")
            apiFuncName = result.group("funcName")

            rowDataBean = RowDataBean()
            rowDataBean.apiCount += 1
            rowDataBean.users = users.value
            rowDataBean.apiType = apiType.value
            rowDataBean.prop = prop.value
            rowDataBean.parentPropCdu = prop.value
            rowDataBean.parentPropIcm = icmFlag + prop.value
            rowDataBean.parentPropAero = aeroFlag + prop.value

            rowDataBean.permission.append(permission.value)
            rowDataBean.setSignal.append(setSignal.value)
            rowDataBean.genCarApi = genCarApi.value != 'No'
        
            # int[] int[12]
            arrayPatter = '(?P<returnType>\w+)\[(?P<count>\d*)\]'
            # 当前API为数组
            if re.match(arrayPatter, apiReturnType):
                result = re.search(arrayPatter, apiReturnType)
                arrayCount = 0 if result.group('count') == '' or result.group('count') is None else result.group('count')
                rowDataBean.isArray = True
            apiReturnType = result.group("returnType")
            dataType = apiReturnType

            # void的为set方法,数据类型需要单独获取
            if apiReturnType == "void":
                result = re.search(returnTypePatter+"\s(?P<funcName>\w+)\((?P<dataType>\w+)", api.value)
                dataType = result.group("dataType") if result is not None else None
                # 当前API为数组
                if re.match(".*(?P<dataType>\w+)\[\d*\]", api.value):
                    rowDataBean.isArray = True

            # 如果prop为空,说明是多个API共有一个prop
            # 一个prop有多个API时,合并单元格导致数据为空
            if prop.value == "":
                parentRowData = findLastProp(rowDataBeanList)
                if parentRowData is not None:
                    rowDataBean.parentPropCdu = parentRowData.prop
                    rowDataBean.parentPropIcm = icmFlag + parentRowData.prop
                    rowDataBean.parentPropAero = aeroFlag + parentRowData.prop
                    rowDataBean.parentCallback = "ID_" + rowDataBean.parentPropCdu if callback.value == "" else callback.value

                    parentRowData.permission.append(permission.value)
                    parentRowData.setSignal.append(setSignal.value)
                else:
                    print("Error : 没有找到父prop : {} {}\n", apiDesc.value, api.value)
            else:
                rowDataBean.callback = "ID_" + rowDataBean.parentPropCdu if callback.value == "" else callback.value
                rowDataBean.parentCallback = rowDataBean.callback

            itemApiDataBean = ApiDataBean()
            itemApiDataBean.returnType = apiReturnType
            itemApiDataBean.dataType = dataType
            itemApiDataBean.apiName = apiFuncName
            itemApiDataBean.jniName = jniApi.value
            itemApiDataBean.apiDesc = apiDesc.value
            itemApiDataBean.paramsDesc = paramsDesc.value
            itemApiDataBean.unit = unit.value
            itemApiDataBean.signal = setSignal.value
            itemApiDataBean.permission = permission.value

            rowDataBean.apiList.append(itemApiDataBean)
            rowDataBeanList.append(rowDataBean)
        else:
            lastRowData = rowDataBeanList[len(rowDataBeanList) - 1]
            lastApiList = lastRowData.apiList[len(lastRowData.apiList) - 1]
            # 判断上一条是否是数组
            if lastRowData.isArray:
                # 复用prop、callback、API等信息
                # jniName直接获取实际值，不做逻辑处理
                itemApiDataBean = copy.deepcopy(lastApiList)
                itemApiDataBean.jniName = jniApi.value
                itemApiDataBean.permission = permission.value
                itemApiDataBean.index = lastRowData.apiCount
                itemApiDataBean.apiDesc = apiDesc.value
                itemApiDataBean.paramsDesc = paramsDesc.value
                itemApiDataBean.unit = unit.value
                itemApiDataBean.signal = setSignal.value

                if prop.value == "":
                    lastRowData.permission.append(permission.value)
                    lastRowData.setSignal.append(setSignal.value)

                lastRowData.apiCount += 1
                lastRowData.apiList.append(itemApiDataBean)
            else:
                raise ValueError("数据异常，请检查")

    return rowDataBeanList


def parseArgs():
    global debugEnable
    global excelPath
    global excelSheetName
    """
    Parse command line commands.
    """
    import argparse
    parse_gen = argparse.ArgumentParser(description="Generate the json file from a xlsx file")
    parse_gen.add_argument("fileName", help="set the xlsx file to generate the json file")
    parse_gen.add_argument("-d", "--debug", dest='debugEnable', help="enable debug info", action='store_true')
    parse_gen.add_argument("-s", "--sheetName", help="set the sheet name of the xlsx file", default=None)
    parse_gen.add_argument("-p", "--project", help="set the project name", default='d55')
    parse_gen.add_argument("-v", "--version", help="set the project version", default='ET1')
    args = parse_gen.parse_args()

    if debugEnable:
        print("%s\n" % (args))

    debugEnable = args.debugEnable
    excelPath = args.fileName
    excelSheetName = args.sheetName
    return args


def app():
    parseArgs()
    # from carapiparser.parser_excel import parseExcel
    # 解析excel
    # rowDataList = parseExcel(excelPath, excelSheetName)
    # if debugEnable:
    #     for rowData in rowDataList:
    #         for cell in rowData.values():
    #             print("rowIndex = %2d cellIndex = %2d title = %10s value = %s" % (
    #                 cell.rowIndex, cell.cellIndex, cell.title, cell.value))
    #         print("\n")
    # dataList = parseRowData(rowDataList)
    # for data in dataList:
    #     print("prop = {} api = {} apiCount = {}".format(data.prop, data.apiList, data.apiCount))

if __name__ == '__main__':
    app()
