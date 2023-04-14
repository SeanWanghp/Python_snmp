import openpyxl

workbook = openpyxl.load_workbook("Testbeds Info.xlsx")
sheet = workbook["Sheet1"]
# rows 按照行获取表单中所有的格子，每一行的数据放到一个元祖中
res = list(sheet.rows)
# 获取excel表格中的第一行的数据，作为字典的key==》生成一个list列表
title = [i.value for i in res[0]]
# 作为每个字典的容器
cases = []
# 遍历第一行意外的所有行
for item in res[1:]:
    # 获取每行的数据
    dataline = [i.value for i in item]
    if all(i is None for i in dataline):
        continue
    # 把遍历的每行数据与第一行title数据打包成字典
    dicline = dict(zip(title, dataline))
    cases.append(dicline)

for item in cases:
    print(item)
