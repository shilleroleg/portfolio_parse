# import pandas as pd
import openpyxl as oxl
import xlrd
from datetime import datetime

import get_file_list as gfl


def parse_excel_report(file_name):
    """Парсим файл с ежедневным отчетом и
     возвращаем словарь с активами assets_dict и словарь с портфелем portfolio_dict"""
    # Возвращаемые словари
    return_assets_dict = {'time_report': [],
                          'incoming_amount': [],
                          'outgoing_amount': [],
                          'credit_customer': [],
                          'credit_corporate': [],
                          'assets_at_start': [],
                          'assets_at_end': []}
    return_portfolio_dict = {}
    # Расширение файла
    file_ext = file_name.split(".")[-1]

    if file_ext == "xls":
        workb = xlrd.open_workbook(file_name)
        # Загружаем активный лист
        ws = workb.sheet_by_index(0)
        # Получаем максимальное количество заполненных строк
        ws_rows = ws.nrows
        xlsx_col = 0                # В openpyxl отсчет столбцов начинается с 1, в xlrd с 0
    elif file_ext == "xlsx":
        workb = oxl.load_workbook(filename=file_name, read_only=True, data_only=True)
        # Загружаем активный лист
        ws = workb.active
        # Получаем максимальное количество заполненных строк
        ws_rows = ws.max_row
        xlsx_col = 1                # В openpyxl отсчет столбцов начинается с 1

    # Пробегаем файл по строчкам
    cur_row = 1
    while cur_row < ws_rows:
        cell_name = "A" + str(cur_row)
        # Дата отчета
        if ws.cell(cur_row, xlsx_col).value == "ПериодДат":
            time_rep = datetime.strptime(ws.cell(cur_row, 3 + xlsx_col).value.split(" ")[-1], '%d.%m.%Y')
            return_assets_dict['time_report'].append(time_rep)
        # Входящая сумма средств на счете
        if ws.cell(cur_row, xlsx_col).value == "100":
            incoming_amount = ws.cell(cur_row, 5 + xlsx_col).value
            return_assets_dict['incoming_amount'].append(incoming_amount)
        # Начислено клиентом и в рамках корпоративных действий
        if ws.cell(cur_row, xlsx_col).value == "230":
            credit_customer = ws.cell(cur_row, 5 + xlsx_col).value
            credit_corporate = ws.cell(cur_row + 1, 5 + xlsx_col).value
            return_assets_dict['credit_customer'].append(credit_customer)
            return_assets_dict['credit_corporate'].append(credit_corporate)
        # Исходящая сумма средств на счете
        if ws.cell(cur_row, xlsx_col).value == "2250":
            outgoing_amount = ws.cell(cur_row, 5 + xlsx_col).value
            return_assets_dict['outgoing_amount'].append(outgoing_amount)
        # Сумма активов на начало и конец дня
        if ws.cell(cur_row, xlsx_col).value == "2600":
            assets_at_start = ws.cell(cur_row, 5 + xlsx_col).value
            assets_at_end = ws.cell(cur_row + 1, 5 + xlsx_col).value
            return_assets_dict['assets_at_start'].append(assets_at_start)
            return_assets_dict['assets_at_end'].append(assets_at_end)
            break                     # Выходим так как достигли конца таблицы со средствами

        cur_row += 1

    return return_assets_dict, return_portfolio_dict


if __name__ == "__main__":
    # Получаем список всех файлов с отчетами
    file_list = gfl.get_file_list("c:\\Users\\olega\\PycharmProjects\\portfolio_parse\\src\\report\\")
    print(file_list)

    for file_n in file_list:
        assets_dict, portfolio_dict = parse_excel_report(file_n)
        print(assets_dict)
