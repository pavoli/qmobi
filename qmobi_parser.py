import urllib.request, urllib.error
import re
import json


CURRENCY_URL = 'https://www.cbr.ru/currency_base/daily/'
REGEXP_TABLE = '<table[^>]*>\s*((?:.|\n)*?)</table>'
pattern_table = re.compile(REGEXP_TABLE)


def parser(from_currency: str, to_currency: str, qty: float) -> str:
    result = {'error': 'No found suitable currency'}

    try:
        html = urllib.request.urlopen(CURRENCY_URL).read().decode('utf-8')
        table = re.findall(pattern_table, html)
        str_data = ''.join(table).split('<tr>')
        found_currency = [i.replace('\r\n', '').replace('</tr>', '').strip() for i in str_data if to_currency in i]
        found_currency = ''.join(found_currency).split('<td>')
        found_currency = [i.strip().replace('</td>', '') for i in found_currency]

        if any(found_currency):
            value = float(found_currency[5].replace(',', '.'))
            rate = int(found_currency[3])
            exchange = qty * value / rate

            result = {
                'original': from_currency,
                'currency': to_currency,
                'qty': qty,
                'result': round(exchange, 2)
            }

        print("Content-type: text/html")
        print()
        print(result)

        return json.dumps(result)
    except urllib.error.HTTPError as e:
        print(str(e))


if __name__ == '__main__':
    parser(from_currency='RUB', to_currency='CZK', qty=1000)
