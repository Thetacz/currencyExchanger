## Currency Exchanger written as Kiwi.com task

It uses fortex-python module to do the heavy lifting. Output is json object writen in console and to file 'exchangex.json'.

note: if it can't find rate on selected currencty, it writes 'rate not available' instead of the exchange rate

# TODO:
 - change source of currency exchange rates to be more realiable
 - add support for currency symbols with more chars
 - speed up computation of exchange()