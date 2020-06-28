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

    def create_table(self, create_dict, type_list, table_name: str):
        """Создаем таблицу с именем table_name и столбцами с именами ключей словаря create_dict,
        типы данных задаются в списке type_list"""

        # execute("CREATE TABLE IF NOT EXISTS assets("
        #         "id integer PRIMARY KEY,"
        #         "time_report CHAR(20),"
        #         "incoming_amount FLOAT,"
        #         "outgoing_amount FLOAT,"
        #         "credit_customer FLOAT,"
        #         "credit_corporate FLOAT,"
        #         "assets_at_start FLOAT,"
        #         "assets_at_end FLOAT)")

        # Fixme
        exec_str = "CREATE TABLE IF NOT EXISTS {0}(id integer PRIMARY KEY".format(table_name)

        for num, key in enumerate(create_dict.keys()):
            exec_str += ", {0} {1}".format(str(key), str(type_list[num]))

        exec_str += ")"

        self.cursor.execute(exec_str)
        # Метод commit() сохраняет все сделанные изменения
        self.connection.commit()

    def insert_data(self, data, table_name: str):
        """Добавляем данные из словаря data в таблицу с именем table_name.
        В словаре значения должны быть списком (даже из одного элемента).
        Если в списке несколько элементов - обходим в цикле.
        Если в списке нет элементов ничего не делаем"""
        # Добавляем только если не пустой словарь
        if tuple(data.values())[0]:
            sql = 'INSERT OR IGNORE INTO {0} ({1}) VALUES ({2})'.format(table_name,
                                                                        ','.join(data.keys()),
                                                                        ','.join(['?'] * len(data)))
            for i in range(len(tuple(data.values())[0])):
                self.cursor.execute(sql, [row[i] for row in tuple(data.values())])
                self.connection.commit()

    def find_duplicates(self, find_table="assets", find_col="time_report"):
        """Ищем строки дубликаты по времени"""
        self.cursor.execute("SELECT id, " + find_col + ", COUNT(*) "
                            "FROM " + find_table +
                            " GROUP BY " + find_col +
                            " HAVING COUNT(*) > 1")
        return self.cursor.fetchall()

    def get_list_filename(self, find_table="assets"):
        """Получаем из базы данных список файлов из которых уже загружены данные"""
        sql_query = "SELECT file_name FROM {0}".format(find_table)
        self.cursor.execute(sql_query)
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


