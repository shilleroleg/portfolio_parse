import sql_database as sq

# TODO добавить рекурсивный вызов функции для удаления более чем одного дубликата за раз
# SELECT `COLUMN` FROM `table` WHERE `COLUMN` IN (SELECT `COLUMN` FROM `table` GROUP BY `COLUMN` HAVING count(*)>1);
def find_and_del_duplicates(f_table, f_col):
    db = sq.SQLiter("portfolio.db")
    ans = db.find_duplicates(find_table=f_table, find_col=f_col)
    print(ans)

    for an in ans:
        ids = an[0]
        find_value = an[1]
        count = an[2]
        db.delete_row(f_table, ids)
        print(ids, count)

    db.close()


if __name__ == "__main__":
    find_and_del_duplicates(f_table="trades", f_col="number_trade")
    find_and_del_duplicates(f_table="assets", f_col="time_report")
