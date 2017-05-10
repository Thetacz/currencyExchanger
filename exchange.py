#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import urllib2
import json
import sys

YAHOO_CURRENCY_CONVERTER_URL = '''
http://finance.yahoo.com/connection/currency-converter-cache?date=
'''
SYMBOLS_URL = "http://www.localeplanet.com/api/auto/currencymap.json"


class Exchange(object):

    def __init__(self, amount, _input, _output):
        self.amount = amount
        if(self.amount is None):
            print("Error: argument --amount is required.")
            sys.exit(1)

        if(_input is None):
            print("Error: argument --input_currency is required.")
            sys.exit(1)
        self.input = _input.upper()

        if(_output):
            self.output = _output.upper()
        else:
            self.output = None

        self.rates = {}
        # get newest rates available
        self._getRates()
        self._loadSymbols()

        self.multiple_input = False
        self.multiple_output = False

    def _getRates(self):
        data = json.loads('[' + "".join(urllib2.urlopen(
                            YAHOO_CURRENCY_CONVERTER_URL
                            )
                        .readlines()[8:-5])
                        .replace("\n", "") + ']')
        if data:
            for x in data:
                _code = x[u"resource"][u"fields"][u"symbol"][:3]
                self.rates[_code] = {
                    u'time': int(x[u"resource"][u"fields"][u"ts"]),
                    u'rate': float(x[u"resource"][u"fields"][u"price"]),
                    u'symbol': None
                }
            return True
        else:
            print("Could not get new rates, using rates in rates.json")
            with open('rates.json') as data_file:
                data = json.load(data_file)
            for x in data:
                self.rates[x] = {
                    u'time': int(x[u"resource"][u"fields"][u"ts"]),
                    u'rate': float(x[u"resource"][u"fields"][u"price"]),
                    u'symbol': None
                }
            return False

    def _loadSymbols(self):
        data = json.loads("".join(urllib2.urlopen(
                            SYMBOLS_URL
                            ).readlines()))
        if data:
            for x in data:
                if x in self.rates:
                    self.rates[x][u'symbol'] = data[x][u'symbol_native']
            return True
        else:
            print("Could not get symbols, using symbols in rates.json")
            with open('rates.json') as data_file:
                data = json.load(data_file)
            for x in data:
                if x in self.rates:
                    self.rates[x][u"symbol"] = (
                        data[x][u"symbol_native"].encode("utf-8")
                        )
            return False

    def _createJsonForm(self):
        self.data = {
                "input": {
                    "amount": round(self.amount, 2),
                },
                "output": {
                }
        }

    def checkCurrencyCode(self, code):
        for x in self.rates:
            if(x == code):
                return True
        return False

    def switchSymbolToCurrencyCode(self, symbol):
        code = []
        for x in self.rates:
            if(self.rates[x][u'symbol']):
                if(self.rates[x][u'symbol'].encode("utf-8") == (
                        symbol.encode("utf-8"))):
                    code.append(x)
        if(code == []):
            raise KeyError("{} not found in known rates".format(symbol))
        return [str(x) for x in code]

    def getRate(self, code):
        return self.rates[code][u'rate']

    def exchange(self, amount, _input, _output):
        input_rate = self.getRate(_input)
        if self.multiple_output:
            for x in _output:
                rate = (self.amount / input_rate) * self.getRate(x)
                self.data[u'output'][x] = round(rate, 2)
        elif not _output:
            for x in self.rates:
                rate = (self.amount / input_rate) * self.getRate(x)
                self.data[u'output'][str(x)] = round(rate, 2)
        else:
            rate = (self.amount / input_rate) * self.getRate(_output)
            self.data[u'output'][_output] = round(rate, 2)

    def fillJson(self):
        try:
            if(not self.checkCurrencyCode(self.input)):
                self.input = self.switchSymbolToCurrencyCode(self.input)
                self.multiple_input = True

            if(not self.checkCurrencyCode(self.output) and self.output):
                    self.output = self.switchSymbolToCurrencyCode(
                        self.output
                        )
                    self.multiple_output = True

            if not self.multiple_input:
                self._createJsonForm()
                self.data['input']['currency'] = self.input
                self.exchange(self.amount, self.input, self.output)
                return self.data
            else:
                data_multiple = []
                for x in self.input:
                    self._createJsonForm()
                    self.data['input']['currency'] = x
                    self.exchange(self.amount, x, self.output)
                    data_multiple.append(self.data)
                return data_multiple
        except:
            e = sys.exc_info()[0]
            print("Error: {}".format(e))
            print("exiting...")
            sys.exit(1)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="This is a currency echanger."
        )

    parser.add_argument("--amount",
                        type=float,
                        help="amount which we want to convert"
                        )
    parser.add_argument("--input_currency",
                        type=str,
                        help="input currency - \
                            3 letters name or currency symbol"
                        )
    parser.add_argument("--output_currency",
                        type=str,
                        help="requested/output currency - \
                            3 letters name or currency symbol"
                        )
    args = parser.parse_args()

    converter = Exchange(args.amount,
                         args.input_currency,
                         args.output_currency
                         )
    data = converter.fillJson()
    print(data)

    with open('exchanged.json', 'w') as outfile:
        json.dump(data, outfile)
