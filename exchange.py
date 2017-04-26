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
            
        self.input = input.upper()
        if self.input is None:
            print("Error: argument --input_currency is required.")
            sys.exit(1)
            
        self.output = output.upper()
            
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
                    code.append(x)     
        return code
    
    def askCurrencyCode(self, symbol):
        output_list = self.switchSymbolToCurrencyCode(symbol)
        if(not len(output_list)):
            raise KeyError
        print("Found more currencies under this symbol.")
        for i,x in enumerate(output_list):
            print("{}: code = {}, name = {}".format(i, str(x['cc'].encode('utf-8')), str(x['name'].encode('utf-8'))))
            x['id'] = i
        vstup = len(output_list)+1
        while(vstup >= len(output_list) or vstup < 0):
            try:
                vstup = int(input("Which one did you mean? (type number)  "))
                if(vstup >= len(output_list) or vstup < 0):
                    print("The number must be inside 0 and {} range".format(len(output_list)-1))
            except NameError:
                print("Must be a number")
            except KeyboardInterrupt:
                print("Interrupted by keyboard, exiting")
                sys.exit(1) 
            except:
                e = sys.exc_info()[0]
                print("Error: %s" % e)
        for key in output_list:
            if key['id'] == vstup:
                return str(key['cc'])
    
    def exchange(self, amount, input, output):
        if(not output):
            print("Converting to all currencies.")
            for i, x  in enumerate(self.currencies):
                try:
                    print("done: {} / {}". format(i, len(self.currencies)-1))
                    self.data['output'][str(x['cc'])] = round(self.converter.convert(input, x['cc'], amount), 2)
                except forex_python.converter.RatesNotAvailableError:
                    self.data['output'][str(x['cc'])] = "rates not avaiable"
        else:            
            return self.converter.convert(input, output, amount)
    
    def fillJson(self):
        try:
            self.data = {
                "input": { 
                    "amount": round(self.amount, 2),
                },
                "output": {
                }
            }
            if(not self.checkCurrencyCode(self.input)):
                self.input = self.askCurrencyCode(self.input)
            self.data['input']['currency'] = self.input
                
            if(not self.checkCurrencyCode(self.output) and self.output):
                self.output = self.askCurrencyCode(self.output)
            print("Converting to specified currency.")
            try:
                if(not self.output):
                    self.exchange(self.amount, self.input, self.output)
                else:
                    self.data['output'][self.output] = round(self.exchange(self.amount, self.input, self.output), 2)
            except forex_python.converter.RatesNotAvailableError: 
                self.data['output'][self.output] = "rates not avaiable"
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

