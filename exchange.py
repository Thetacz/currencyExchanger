#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import json
from currency_converter import CurrencyConverter
from exceptions import NotImplementedError
import sys

class Exchange(object):
    def __init__(self, amount, input, output):
        
        self.amount = amount
        if self.amount is None:
            print("Error: argument --amount is required.")
            sys.exit(1)
            
        self.input = input
        if self.input is None:
            print("Error: argument --input_currency is required.")
            sys.exit(1)
            
        self.output = output
        self.converter = CurrencyConverter()
    
    def exchange(self, amount, input, output):
        if(not self.output):
            self.to_all = True
            print("Converting to all currencies.")
            raise NotImplementedError, "Not implemented yet!"
        else:
            print("Converting to specified currency.")
            return self.converter.convert(amount, input, output)
    
    def fill_json(self):
        try:
            self.data = {
                "input": { 
                    "amount": "{0:.2f}".format(self.amount),
                    "currency": self.input
                },
                "output": {
                    self.output : "{0:.2f}".format(self.exchange(self.amount, self.input, self.output))
                }
            }
        except NotImplementedError:
            print("Error: Not implemented yet!")
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
    data = converter.fill_json()
    print(data)      
        
    with open('exchanged.json', 'w') as outfile:
        json.dump(data, outfile)

