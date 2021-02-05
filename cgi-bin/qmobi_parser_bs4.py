import requests
import json
from bs4 import BeautifulSoup


CURRENCY_URL = 'https://www.cbr.ru/currency_base/daily/'


def parser(from_currency: str, to_currency: str, qty: float) -> json:
    result = {'error': 'No found suitable currency'}

    try:
        source = requests.get(CURRENCY_URL)

        if source.status_code == 200:
            source_text = source.text
            parsed_text = BeautifulSoup(source_text, features='html.parser')
            table_data = parsed_text.findAll('tr')
            currency = [i.text.split('\n') for i in table_data if to_currency in i.text.split('\n')]
            # currency_dict = dict((i[2], {'code': i[1], 'name': i[4], 'rate': i[3], 'value': i[5]}) for i in currency)

            if currency:
                value = float(currency[0][5].replace(',', '.'))
                rate = int(currency[0][3])

                result = {
                    'original': from_currency,
                    'currency': to_currency,
                    'qty': qty,
                    'result': qty * value / rate
                }

            print("Content-type: text/html")
            print()
            print(result)

            return json.dumps(result)

    except requests.ConnectionError as e:
        print(str(e))


if __name__ == '__main__':
    parser(from_currency='RUB', to_currency='EUR', qty=2500)
