import json
import requests


def get_info(ticker):
    req_str = 'https://iss.moex.com/iss/engines/' + \
              'stock/markets/shares/boards/tqbr/' + \
              'securities/{0}.json?iss.meta=off'.format(ticker)

    # response = pd.read_json(req_str)

    req = requests.get(req_str)
    response = json.loads(req.text)

    sec_columns = response['securities']['columns']
    sec_data = response['securities']['data'][0]

    # market_columns = response['marketdata']['columns']
    # market_data = response['marketdata']['data'][0]
    #
    # for i in range(len(sec_columns)):
    #     print(sec_columns[i] + ': ' + str(sec_data[i]))

    tiker = sec_data[0]
    shortname = sec_data[2]
    lot_size = sec_data[4]
    status = sec_data[6]
    isin = sec_data[19]
    reg_number = sec_data[21]

    print(isin)


if __name__ == "__main__":
    get_info('RSTI')
