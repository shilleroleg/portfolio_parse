# import pandas as pd
import openpyxl as oxl
import xlrd
from datetime import datetime

import get_file_list as gfl
import sql_database as sq


def parse_excel_report(file_name_parse):
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
    file_ext = file_name_parse.split(".")[-1]

    if file_ext == "xls":
        workb = xlrd.open_workbook(file_name_parse)
        # Загружаем активный лист
        ws = workb.sheet_by_index(0)
        # Получаем максимальное количество заполненных строк
        ws_rows = ws.nrows
        xlsx_col = 0                # В openpyxl отсчет столбцов начинается с 1, в xlrd с 0
    elif file_ext == "xlsx":
        workb = oxl.load_workbook(filename=file_name_parse, read_only=True, data_only=True)
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
            time_rep = datetime.strptime(ws.cell(cur_row, 3 + xlsx_col).value.split(" ")[-1], '%d.%m.%Y')  # In datetime
            return_assets_dict['time_report'] = time_rep.strftime('%d.%m.%Y')                        # In str
        # Входящая сумма средств на счете
        if ws.cell(cur_row, xlsx_col).value == "100":
            incoming_amount = ws.cell(cur_row, 5 + xlsx_col).value
            return_assets_dict['incoming_amount'] = incoming_amount
        # Начислено клиентом и в рамках корпоративных действий
        if ws.cell(cur_row, xlsx_col).value == "230":
            credit_customer = ws.cell(cur_row, 5 + xlsx_col).value
            credit_corporate = ws.cell(cur_row + 1, 5 + xlsx_col).value
            return_assets_dict['credit_customer'] = credit_customer
            return_assets_dict['credit_corporate'] = credit_corporate
        # Исходящая сумма средств на счете
        if ws.cell(cur_row, xlsx_col).value == "2250":
            outgoing_amount = ws.cell(cur_row, 5 + xlsx_col).value
            return_assets_dict['outgoing_amount'] = outgoing_amount
        # Сумма активов на начало и конец дня
        if ws.cell(cur_row, xlsx_col).value == "2600":
            assets_at_start = ws.cell(cur_row, 5 + xlsx_col).value
            assets_at_end = ws.cell(cur_row + 1, 5 + xlsx_col).value
            return_assets_dict['assets_at_start'] = assets_at_start
            return_assets_dict['assets_at_end'] = assets_at_end
            break                     # Выходим так как достигли конца таблицы со средствами

        cur_row += 1
    # В старых отчетах исходящий остаток не приводился, присваиваем как входящий остаток
    if return_assets_dict['incoming_amount'] and not return_assets_dict['outgoing_amount']:
        return_assets_dict['outgoing_amount'] = return_assets_dict['incoming_amount']

    return return_assets_dict, return_portfolio_dict


if __name__ == "__main__":
    # Получаем список всех файлов с отчетами
    file_list = gfl.get_file_list("c:\\Users\\olega\\PycharmProjects\\portfolio_parse\\src\\report\\")
    # file_list = gfl.get_file_list("d:\\olega\\Финансы\\Брокер\\Отчеты ПСБ\\")
    # print(file_list)

    # db = sq.SQLiter("portfolio.db")
    # db.create_table()

    for count, file_n in enumerate(file_list):
        assets_dict, portfolio_dict = parse_excel_report(file_n)
        print(assets_dict)
        # db.insert_data(assets_dict)
        file_name = file_n.split("\\")[-1]
        print(f"Отчет № {str(count)} из {len(file_list)} - {file_name}")
    #
    # db.close()
