import datetime

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


def get_trades(type_trades="buy"):
    db = sq.SQLiter("portfolio.db")
    ans = db.get_trade_data(table_name="trades", col_name="type_trade", need_data="buy")
    # Сортируем полученные данные по дате
    ans.sort(key=lambda tup: datetime.datetime.strptime(tup[1], '%d.%m.%Y %H:%M:%S'))

    trades = {}

    for an in ans:
        isin = an[5]
        if isin not in trades.keys():
            trade = {"name_paper": an[4],
                     "number_trade": [an[3]],
                     "date_time_trade": [an[1]],
                     "volume": [an[8]],
                     "transac_price": [an[9]]}

            trades[isin] = trade
        else:
            trades[isin]["number_trade"].append(an[3])
            trades[isin]["date_time_trade"].append(an[1])
            trades[isin]["volume"].append(an[8])
            trades[isin]["transac_price"].append(an[9])

    return trades


if __name__ == "__main__":
    # find_and_del_duplicates(f_table="trades", f_col="number_trade")
    # find_and_del_duplicates(f_table="assets", f_col="time_report")
    trades_buy = get_trades("buy")
    print(trades_buy["RU000A0JP5V6"])

