import datetime

import sql_database as sq


# TODO добавить рекурсивный вызов функции для удаления более чем одного дубликата за раз
# SELECT `COLUMN` FROM `table` WHERE `COLUMN` IN (SELECT `COLUMN` FROM `table` GROUP BY `COLUMN` HAVING count(*)>1);
def find_and_del_duplicates(f_table, f_col):
    db = sq.SQLiter("portfolio.db")
    ans = db.find_duplicates(find_table=f_table, find_col=f_col)
    # print(ans)

    for an in ans:
        ids = an[0]
        find_value = an[1]
        count = an[2]
        db.delete_row(f_table, ids)
        print(ids, count)

    db.close()


def get_trades(type_trades="buy"):
    db = sq.SQLiter("portfolio.db")
    ans = db.get_trade_data(table_name="trades", col_name="type_trade", need_data=type_trades)
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
                     "transact_price": [an[9]]}

            trades[isin] = trade
        else:
            trades[isin]["number_trade"].append(an[3])
            trades[isin]["date_time_trade"].append(an[1])
            trades[isin]["volume"].append(an[8])
            trades[isin]["transact_price"].append(an[9])

    return trades


def create_portfolio_from_buy_sell(trades_buy, trades_sell):
    buy_keys = trades_buy.keys()
    sell_keys = trades_sell.keys()

    # print(buy_keys)

    temp_portfolio = {}
    full_portfolio = {}

    # Записываем все покупки
    # Если бумага продавалась, записываем объем как разницу между покупкой и продажей
    for buy_key in buy_keys:
        vol_buy = sum(trades_buy[buy_key]["volume"])
        if buy_key in sell_keys:
            vol_sell = sum(trades_sell[buy_key]["volume"])
        else:
            vol_sell = 0
        temp_portfolio[buy_key] = {"name_paper": trades_buy[buy_key]["name_paper"],
                                   "volume": vol_buy - vol_sell}

    # Из временного словаря в постоянный переносим только записи, где не все бумаги проданы (volume > 0)
    for tp in temp_portfolio.keys():
        if temp_portfolio[tp]["volume"] != 0:
            full_portfolio.update({tp: {"name_paper": temp_portfolio[tp]["name_paper"],
                                        "volume": temp_portfolio[tp]["volume"]}})

    print(full_portfolio)


if __name__ == "__main__":
    # find_and_del_duplicates(f_table="trades", f_col="number_trade")
    # find_and_del_duplicates(f_table="assets", f_col="time_report")
    #
    trades_buy = get_trades("buy")
    trades_sell = get_trades("sell")

    create_portfolio_from_buy_sell(trades_buy, trades_sell)

