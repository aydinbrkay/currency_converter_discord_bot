import discord
from discord.ext import commands
from forex_python.converter import CurrencyRates, CurrencyCodes
import re

currencyRate = CurrencyRates()
currencyCode = CurrencyCodes()

currencies = str(currencyRate.get_rates("USD"))  # Turning into string to extract currencies
currencies = currencies.replace("{", "")  # Getting rid of '{' at the start
currencies = currencies.replace("}", "")  # Getting rid of '}' at the end
# String is in 'CURRENCY': 1.23131 ... format right now
currencyList = currencies.split()
allCurrencies = []
count = 0
while count <= len(currencyList)-1:
    allCurrencies.append(re.search("'(.*?)'", currencyList[count]).group(1))  # Extracting currencies which are between ''
    count = count + 2  # Here +2 because every even index holds currencies.Odd ones hold numbers which we want to get rid of
allCurrencies.append("USD")  # Adding USD at the end because we used it to get all the other currencies

client = commands.Bot(command_prefix=">")


@client.event
async def on_ready():
    print("Currency Converter Bot is online and ready")


@client.command()
async def commands(ctx):
    await ctx.send("Available commands are: \n"
                   + ">currencylist : Lists all available currencies and their names. \n"
                   + ">currencyname : Gives you full name and symbol of a currency. \n"
                   + ">convert : Converts between 2 currencies for given amount. \n"
                   + ">clear : Clears all messages in the text channel including bot itself and users' (up to 100 messages)"
                   + "If there is no given amount then converts for 1 by default. \n"
                   + "Example usage of >convert : \n>convert USD to EUR OR >convert 10 USD to EUR")


@client.command()
async def clear(ctx):
    await ctx.channel.purge()


@client.command()
async def convert(ctx, *, string):
    string = string.upper()
    input = string.split()
    if len(input) == 3: # If user doesn't give a specific amount
        if allCurrencies.__contains__(input[0]) and allCurrencies.__contains__(input[2]): # Checking if input currencies exist
            await ctx.send("1 " + currencyCode.get_currency_name(input[0]) + " = " +
                        str(currencyRate.get_rate(input[0], input[2])) + " " + currencyCode.get_currency_name(input[2]))
        else:
            await ctx.send("Currencies are wrong or doesn't supported.Please try again")
    elif len(input) == 4:  # If user gives a specific amount
        if allCurrencies.__contains__(input[1]) and allCurrencies.__contains__(input[3]): # Checking if input currencies exist
            await ctx.send(input[0] + " " + currencyCode.get_currency_name(input[1]) + " = " +
                        str(currencyRate.convert(input[1], input[3], int(input[0]))) + " " + currencyCode.get_currency_name(input[3]))
        else:
            await ctx.send("Currencies are wrong or doesn't supported.Please try again")
    else:
        await ctx.send("Something is wrong with your input!Please try again")


@client.command()
async def currencylist(ctx):
    temp = "List of available currencies: "
    for currency in allCurrencies:
        temp = temp + "\n" + currency + " / " + currencyCode.get_symbol(currency) + " / "+str(currencyCode.get_currency_name(currency))
    await ctx.send(temp)


@client.command()
async def currencyname(ctx, currency):
    currency = currency.upper()
    if allCurrencies.__contains__(currency):
        await ctx.send(currency + " / " + currencyCode.get_symbol(currency) + " / " + currencyCode.get_currency_name(currency))
    else:
        await ctx.send("This currency doesn't exist.Please try again")

# !!!!!!!!!!!
client.run("YOUR KEY HERE")  # REPLACE PARAMETER WITH YOUR OWN KEY
