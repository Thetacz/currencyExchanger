#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import json
from currency_converter import CurrencyConverter

class Exchange(object):
    def __init__(self, amount, input, output):
        self.amount = amount
        self.input = input
        self.output = output
        self.converter = CurrencyConverter()
    
    def exchange(self):
        return self.converter.convert(self.amount, self.input, self.output)
        
    

if __name__ == "__main__":    
    
    parser = argparse.ArgumentParser(description="This is a currency echanger.")
    
    parser.add_argument("--amount", type=float, help="amount which we want to convert")
    parser.add_argument("--input_currency", type=str, help="input currency - 3 letters name or currency symbol")     
    parser.add_argument("--output_currency", type=str, help="requested/output currency - 3 letters name or currency symbol")   
    args = parser.parse_args()

    converter = Exchange(args.amount, args.input_currency, args.output_currency)
    print(converter.exchange())
    
    data = {
        "input": { 
            "amount": args.amount,
            "currency": args.input_currency
        },
        "output": {
            args.output_currency : args.amount
        }
    }
        
    with open('exchanged.json', 'w') as outfile:
        json.dump(data, outfile)

