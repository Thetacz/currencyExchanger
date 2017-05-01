## Currency Exchanger written as Kiwi.com task

Uses YAHOO financial rates and symbols from localeplanet.com. If it can't connect, uses local copy in 'rates.json'.

Params:

	--amount			amount of currency to be exchanged
	
	--input_currency	code or symbol of currency to be achanged
	
	--output_currency	code or symbol of currency to exchange to (if not provided will convert to all known currencies)
	
Output is json object writen in console and to file 'exchanged.json'.

note: If you use symbol that matches more currencies, it converts to them all.