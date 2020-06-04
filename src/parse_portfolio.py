# import pandas as pd
#
portfolio_file_name = "c:\\Users\\olega\\PycharmProjects\\portfolio_parse\\src\\report\\18645(19-03-2020)05-23.xlsx"
#
# port = pd.read_excel(portfolio_file_name, header=None, sheet_name=0, skiprows=6, convert_float=False)
#
# # количество строк и количество столбцов в таблице
# p_str = port.shape[0]
# p_col = port.shape[1]
#
# print(port.head())

# for i in range(p_str-1):
#     print(port[i:i+1])

import openpyxl as oxl
from datetime import datetime

workb = oxl.load_workbook(filename=portfolio_file_name, data_only=True)
# Загружаем активный лист
ws = workb.active

ws_rows = ws.max_row

print(ws.dimensions)

cur_row = 1
while cur_row < ws_rows:
    cell_name = "A" + str(cur_row)
    # Дата отчета
    if ws[cell_name].value == "ПериодДат":
        time_rep = datetime.strptime(ws.cell(row=cur_row, column=4).value[2:12], '%d.%m.%Y')

    # Входящая сумма средств на счете
    if ws[cell_name].value == "100":
        incom_amount = ws.cell(row=cur_row, column=6).value
    # Pачислено клиентом и в рамках корпоративных действий
    if ws[cell_name].value == "230":
        credit_customer = ws.cell(row=cur_row, column=6).value
        credit_corporate = ws.cell(row=cur_row + 1, column=6).value
    # Исходящая сумма средств на счете
    if ws[cell_name].value == "2250":
        outgoing_amount = ws.cell(row=cur_row, column=6).value
    # Сумма активов на начало и конец дня
    if ws[cell_name].value == "2600":
        active_at_start = ws.cell(row=cur_row, column=6).value
        active_at_end = ws.cell(row=cur_row + 1, column=6).value





    cur_row += 1

