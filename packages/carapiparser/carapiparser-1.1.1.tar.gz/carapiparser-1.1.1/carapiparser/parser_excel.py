# coding=utf-8
import copy
import xlrd
from .format_api import parseRowData

debugEnable = False
sheetNameDefault = "0.7"
firstRowName = "使用方"


class CellData:
    def __init__(self, title, cellIndex=-1, rowIndex=-1, value=-1):
        """
        每一个格子
        :param title:标题
        :param rowIndex:列索引
        :param lineIndex: 第几行
        :param value: 当前值
        """
        self.title = title
        self.cellIndex = cellIndex
        self.rowIndex = rowIndex
        self.value = value


def parseExcelTitle(sheet, headerRowIndex):
    """
    解析标题，格式化去年\n
    :param sheet:
    :param headerRowIndex:
    :return:
    """
    rowData = {}
    for colIndex in range(0, sheet.ncols):
        value = sheet.row_values(headerRowIndex)[colIndex]
        if value != "":
            value = str(value).replace("\n", "")
            # print(value)
            rowData[value] = CellData(value, colIndex, headerRowIndex)
            # for rowData
    print("parse excel title suc")
    return rowData


def parseExcelContent(title, sheet, startRow):
    rowDataList = []
    for row in range(startRow, sheet.nrows):
        for item in title.values():
            item.value = sheet.row_values(row)[item.cellIndex]
            item.rowIndex = row
        rowDataList.append(copy.deepcopy(title))
    return rowDataList


def parseExcel(path, sheetName, firstRowFlag=""):
    if sheetName is None:
        sheetName = sheetNameDefault
    if firstRowFlag is not None:
        firstRowName = firstRowFlag
    rowDataList = []
    try:
        with xlrd.open_workbook(path) as book:
            sheet = book.sheet_by_name(sheetName)
            if debugEnable:
                print("parse sheets: ", sheet)

            headerRowIndex = 0xFFFF
            for rowIndex in range(0, sheet.nrows):
                if firstRowName in sheet.row_values(rowIndex)[0].replace("\n", ""):
                    headerRowIndex = rowIndex
                    break
            if headerRowIndex == 0xFFFF:
                raise ValueError("Can't find " + firstRowName + " in this sheet")
            title = parseExcelTitle(sheet, headerRowIndex)
            rowDataList = parseExcelContent(title, sheet, headerRowIndex + 1)
    except IOError as e:
        print("Error------------" + e)
    except xlrd.biffh.XLRDError as e:
        print("Error------------" + e)
    else:
        print("parse excel title suc")
    return rowDataList


def parseRowDataList(rowDataList):
    """
    解析CarApi
    :param rowDataList:
    :return:
    """
    return parseRowData(rowDataList)


def parseArgs():
    """
    Parse command line commands.
    """
    import argparse

    parse_gen = argparse.ArgumentParser(
        description="Generate the json file from a xlsx file"
    )
    parse_gen.add_argument(
        "fileName", help="set the xlsx file to generate the json file"
    )
    parse_gen.add_argument(
        "-d",
        "--debug",
        dest="debugEnable",
        help="enable debug info",
        action="store_true",
    )
    parse_gen.add_argument(
        "-s", "--sheetName", help="set the sheet name of the xlsx file", default=None
    )
    parse_gen.add_argument(
        "-p", "--project", help="set the project name", default="d55"
    )
    parse_gen.add_argument(
        "-v", "--version", help="set the project version", default="ET1"
    )
    args = parse_gen.parse_args()
    if debugEnable:
        print("%s\n" % (args))
    return args


def app():
    args = parseArgs()
    global debugEnable
    debugEnable = args.debugEnable
    if debugEnable:
        print("%s\n" % (args))
    rowDataList = parseExcel(args.fileName, args.sheetName)
    if debugEnable:
        for rowData in rowDataList:
            for cell in rowData.values():
                print(
                    "rowIndex = %2d cellIndex = %2d title = %10s value = %s"
                    % (cell.rowIndex, cell.cellIndex, cell.title, cell.value)
                )
            print("\n")


if __name__ == "__main__":
    app()
