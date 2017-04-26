#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import json
import forex_python
from forex_python.converter import CurrencyRates
from exceptions import NotImplementedError
import sys
import os

# USAGE EXAMPLE:     
# python RocketMap\_git\currencyExchanger\exchange.py --amount 100 --input_currency EUR --output_currency CZK

class Exchange(object):
    def __init__(self, amount, input, output):
        
        with open(os.path.dirname(os.path.abspath(forex_python.__file__)) + '/raw_data/currencies.json', 'r') as f:
            self.currencies = json.loads(f.read())
            
        self.amount = amount
        if self.amount is None:
            print("Error: argument --amount is required.")
            sys.exit(1)
            
        self.input = input
        if self.input is None:
            print("Error: argument --input_currency is required.")
            sys.exit(1)
            
        self.output = output
        self.converter = CurrencyRates()
    
    def checkCurrencyCode(self, code):
        for x in self.currencies:
            if(x['cc'] == code):
                return True
        return False
                    
    def switchSymbolToCurrencyCode(self, symbol):
        code = []
        for x in self.currencies:
            for i in (x['symbol']).encode('utf-8'):
                if(i == symbol):
                    code.append(str(x['cc']))       
        return code
    
    def exchange(self, amount, input, output):
        if(not self.output):
            self.to_all = True
            print("Converting to all currencies.")
            raise NotImplementedError, "Not implemented yet!"
        else:
            print("Converting to specified currency.")
            return self.converter.convert(input, output, amount)
    
    def fillJson(self):
        try:
            self.data = {
                "input": { 
                    "amount": "{0:.2f}".format(self.amount),
                    "currency": self.input
                },
                "output": {
                }
            }
            if(self.checkCurrencyCode(self.output)):
                self.data['output'][self.output] = "{0:.2f}".format(self.exchange(self.amount, self.input, self.output)) 
            else:
                self.output_list = self.switchSymbolToCurrencyCode(self.output)
                for x in self.output_list:
                    self.data['output'][x] = "{0:.2f}".format(self.exchange(self.amount, self.input, x))
                
        except NotImplementedError:
            print("Error: Not implemented yet!")
            sys.exit(1)   
        except KeyError:
            print("Error: used unknown currency")
            sys.exit(1)    
        except:
            e = sys.exc_info()[0]
            print("Error: %s" % e)
            sys.exit(1)           
        return self.data
                

if __name__ == "__main__":    
    
    parser = argparse.ArgumentParser(description="This is a currency echanger.")
    
    parser.add_argument("--amount", type=float, help="amount which we want to convert")
    parser.add_argument("--input_currency", type=str, help="input currency - 3 letters name or currency symbol")     
    parser.add_argument("--output_currency", type=str, help="requested/output currency - 3 letters name or currency symbol")   
    args = parser.parse_args()

    converter = Exchange(args.amount, args.input_currency, args.output_currency)
    data = converter.fillJson()
    print(data)      
        
    with open('exchanged.json', 'w') as outfile:
        json.dump(data, outfile)

