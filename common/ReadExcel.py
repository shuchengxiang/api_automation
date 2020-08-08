import xlrd
import os


class ReadExcel:

    def __init__(self, file_name=None, sheet_name=None):
        if file_name:
            self.file_name = file_name
            self.sheet_name = sheet_name
        else:
            self.file_name = os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), "data"), "apiTest.xlsx")
            self.sheet_name = 'Sheet1'
        self.data = self.get_data()

    def get_all_data(self):
        data = xlrd.open_workbook(self.file_name)
        table = data.sheet_by_name(self.sheet_name)

        # 获取总行数、总列数
        nrows = table.nrows
        ncols = table.ncols
        if nrows > 1:
            # 获取第一列的内容，列表格式
            keys = table.row_values(0)
            listApiData = []
            # 获取每一行的内容，列表格式
            for col in range(1, nrows):
                values = table.row_values(col)
                # keys，values这两个列表一一对应来组合转换为字典
                api_dict = dict(zip(keys, values))
                listApiData.append(api_dict)
            return listApiData
        else:
            print("表格未填写数据")
            return None
            # 获取sheets的内容

    def get_data(self):
        data = xlrd.open_workbook(self.file_name)
        tables = data.sheet_by_name(self.sheet_name)
        return tables

    # 获取单元格的行数
    def get_lines(self):
        tables = self.data
        return tables.nrows

    # 获取某一个单元格的内容
    def get_cell_value(self, row, col):
        tables = self.data
        cell = tables.cell_value(row, col)
        return cell

    # 根据对应case_id找到对应行的内容
    def get_rows_data(self, case_id):
        row_num = self.get_row_num(case_id)
        self.get_row_values(row_num)

    # 根据对应的case_id找到对应的行号
    def get_row_num(self, case_id):
        num = 0
        coldata = self.get_col_values()
        for data in coldata:
            if case_id in data:
                return num
            num += 1
        return num

    # 根据行号，找到该行的数据
    def get_row_values(self, row):
        tables = self.data
        row_data = tables.row_values(row)
        return row_data

    # 根据列号，找到该列的数据
    def get_col_values(self, col=None):
        if col != None:
            col_data = self.data.col_values(col)
        else:
            col_data = self.data.col_values(0)
        return col_data

if __name__ == '__main__':
    path = os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), "excel_data"), "apiTest.xlsx")
    print(path)
    s = ReadExcel(path, "Sheet1").get_all_data()
    print(s)











