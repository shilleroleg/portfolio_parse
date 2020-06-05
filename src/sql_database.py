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
                            "time_report CHAR(100),"
                            "incoming_amount FLOAT,"
                            "outgoing_amount FLOAT,"
                            "credit_customer FLOAT,"
                            "assets_at_start FLOAT,"
                            "assets_at_end FLOAT)")
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
                                       "assets_at_start,"
                                       "assets_at_end) VALUES(?,?,?,?,?,?)",
                                       (data["time_report"],
                                        data["incoming_amount"],
                                        data["outgoing_amount"],
                                        data["credit_customer"],
                                        data["assets_at_start"],
                                        data["assets_at_end"],))

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
#     # сохраняем данные в переменную
#     table = cursor_obj.fetchall()
#     return table
#
#
# def sql_select_flag(connect, id_for_flag):
#     cursor_obj = connect.cursor()
#     #  извлекаем данные из БД
#     cursor_obj.execute('SELECT weather_flag FROM weather where id = ' + str(id_for_flag))
#     # сохраняем данные в переменную
#     flag = cursor_obj.fetchall()
#     if len(flag) > 0:
#         return flag[0][0]
#     else:
#         return None


if __name__ == "__main__":
    db = SQLiter("my.db")
    db.create_table()

    portfolio_dict = {'time_report': "(2019, 7, 15, 0, 0)",
                      'incoming_amount': 24699.31,
                      'outgoing_amount': 20106.72,
                      'credit_customer': 0,
                      'credit_corporate': 968.64,
                      'assets_at_start': 241779.06,
                      'assets_at_end': 241515.09}

    db.insert_data(portfolio_dict)

    db.close()


