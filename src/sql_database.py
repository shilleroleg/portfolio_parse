import sqlite3
from sqlite3 import Error


class SQLiter:

    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        #  By default, check_same_thread is True and only the creating thread may use the connection.
        #  If set False, the returned connection may be shared across multiple threads.
        #  When using multiple threads with the same connection writing operations should be serialized
        #  by the user to avoid data corruption
        self.connection = sqlite3.connect(database, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def create_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS assets("
                            "id integer PRIMARY KEY,"
                            "time_report CHAR(64),"
                            "incoming_amount FLOAT,"
                            "outgoing_amount FLOAT,"
                            "credit_customer FLOAT,"
                            "credit_corporate FLOAT,"
                            "assets_at_start FLOAT,"
                            "assets_at_end FLOAT)")
        # Метод commit() сохраняет все сделанные изменения
        self.connection.commit()

    def create_table_trade(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS trades("
                            "id integer PRIMARY KEY,"
                            "date_time_trade CHAR(64),"
                            "date_time_execution CHAR(64),"
                            "number_trade BIGINT,"
                            "name_paper CHAR(256),"
                            "isin CHAR(64),"
                            "reg_num CHAR(64),"
                            "type_trade CHAR(8),"
                            "volume INT,"
                            "transac_price FLOAT,"
                            "transac_amount FLOAT,"
                            "nkd FLOAT,"
                            "commission_ts FLOAT,"
                            "commission_klir FLOAT,"
                            "commission_its FLOAT,"
                            "commission_brok FLOAT)")
        # Метод commit() сохраняет все сделанные изменения
        self.connection.commit()

    def insert_data(self, data):
        """Добавляем данные за один день"""
        with self.connection:
            return self.cursor.execute("INSERT OR IGNORE INTO assets("
                                       "time_report,"
                                       "incoming_amount,"
                                       "outgoing_amount,"
                                       "credit_customer,"
                                       "credit_corporate,"
                                       "assets_at_start,"
                                       "assets_at_end) VALUES(?,?,?,?,?,?,?)",
                                       (data["time_report"],
                                        data["incoming_amount"],
                                        data["outgoing_amount"],
                                        data["credit_customer"],
                                        data["credit_corporate"],
                                        data["assets_at_start"],
                                        data["assets_at_end"]))

    def insert_data_trade(self, data):
        """Добавляем сделки"""
        # Добавляем только если не пустой словарь
        if list(data.values())[0]:
            print(data['date_time_trade'])
            for i in range(len(data['date_time_trade'])):
                print(len(data['date_time_trade']), i)
                self.cursor.execute("INSERT OR IGNORE INTO trades("
                                    "date_time_trade,"
                                    "date_time_execution,"
                                    "number_trade,"
                                    "name_paper,"
                                    "isin,"
                                    "reg_num,"
                                    "type_trade,"
                                    "volume,"
                                    "transac_price,"
                                    "transac_amount,"
                                    "nkd,"
                                    "commission_ts,"
                                    "commission_klir,"
                                    "commission_its,"
                                    "commission_brok) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                                    (data['date_time_trade'][i],
                                     data['date_time_execution'][i],
                                     data['number_trade'][i],
                                     data['name_paper'][i],
                                     data['isin'][i],
                                     data['reg_num'][i],
                                     data['type_trade'][i],
                                     data['volume'][i],
                                     data['transac_price'][i],
                                     data['transac_amount'][i],
                                     data['nkd'][i],
                                     data['commission_ts'][i],
                                     data['commission_klir'][i],
                                     data['commission_its'][i],
                                     data['commission_brok'][i]))
                self.connection.commit()

    def find_duplicates(self, find_table="assets", find_col="time_report"):
        """Ищем строки дубликаты по времени"""
        self.cursor.execute("SELECT id, " + find_col + ", COUNT(*) "
                            "FROM " + find_table +
                            " GROUP BY " + find_col +
                            " HAVING COUNT(*) > 1")
        return self.cursor.fetchall()

    def delete_row(self, del_table, del_id):
        """Удаляем строку из таблицы del_table по id del_id"""
        sql_delete_query = "DELETE FROM " + del_table + " WHERE id = " + str(del_id)
        self.cursor.execute(sql_delete_query)
        self.connection.commit()

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()


# def sql_update(connect, val, id_for_upd):
#     # Для обновления будем использовать инструкцию UPDATE.
#     # Также воспользуемся предикатом WHERE в качестве условия для выбора нужного сотрудника.
#     cursor_obj = connect.cursor()
#     string_for_update = 'UPDATE weather SET weather_flag = ' + str(val) + ' where id = ' + str(id_for_upd)
#     print(string_for_update)
#     cursor_obj.execute('UPDATE weather SET weather_flag = ' + str(val) + ' where id = ' + str(id_for_upd))
#     connect.commit()
#
#
# def sql_select(connect):
#     cursor_obj = connect.cursor()
#     #  извлекаем данные из БД
#     cursor_obj.execute('SELECT * FROM weather')
# # #     cursor_obj.execute('SELECT weather_flag FROM weather where id = ' + str(id_for_flag))
#     сохраняем данные в переменную
#     table = cursor_obj.fetchall()
#     return table
#

if __name__ == "__main__":
    db = SQLiter("portfolio.db")
    # db.create_table()

    # portfolio_dict = {'time_report': "(2019, 7, 15, 0, 0)",
    #                   'incoming_amount': 24699.31,
    #                   'outgoing_amount': 20106.72,
    #                   'credit_customer': 0,
    #                   'credit_corporate': 968.64,
    #                   'assets_at_start': 241779.06,
    #                   'assets_at_end': 241515.09}
    #
    # db.insert_data(portfolio_dict)

    portfolio_dict = {'time_report': None,
                      'incoming_amount': 10,
                      'outgoing_amount': None,
                      'credit_customer': 15,
                      'credit_corporate': None,
                      'assets_at_start': None,
                      'assets_at_end': None}
    flag = False
    for pd in portfolio_dict.keys():
        flag += bool(portfolio_dict[pd])
    print(flag)

    if flag < len(portfolio_dict.keys()):
        print("!!")


    # db.insert_data(portfolio_dict)

    # ans = db.find_duplicates(find_table="assets", find_col="time_report")
    # print(ans)
    #
    # for an in ans:
    #
    #     ids = an[0]
    #     times = an[1]
    #     count = an[2]
    #     db.delete_row("assets", ids)
    #     print(ids, count)

    db.close()


