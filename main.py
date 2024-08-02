"""Main module"""

import asyncio
from datetime import datetime

import pandas as pd

from fetch_data import fetch_stock_data, save_to_excel
from candle_chart_creation import draw_candle_chart


def validate_stock_symbol(symbol: str) -> bool:
    """Validate the stock symbol.
    
    :param `str` symbol: The stock symbol to validate.
    
    :return: True if the symbol is valid, False otherwise.
    :rtype: bool
    """
    return len(symbol) == 3


def validate_date(date_str: str) -> bool:
    """Validate the date format and value.
    
    :param `str` date_str: The date string to validate.
    
    :return: True if the date is valid, False otherwise.
    :rtype: bool
    """
    try:
        datetime.strptime(date_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False


async def main():
    """
    Main function to fetch stock data and save it to an Excel file.
    """
    while True:
        stock_symbol = (
            input("Enter the stock symbol (3 alphabetic characters): ").strip().upper()
        )
        if not validate_stock_symbol(stock_symbol):
            print("Invalid stock symbol. It must be exactly 3 characters.")
            continue
        start_date = input("Enter the start date (dd/mm/yyyy): ").strip()
        if not validate_date(start_date):
            print("Invalid start date format. It must be in the format dd/mm/yyyy.")
            continue
        end_date = input("Enter the end date (dd/mm/yyyy): ").strip()
        if not validate_date(end_date):
            print("Invalid end date format. It must be in the format dd/mm/yyyy.")
            continue
        # If all inputs are valid, break the loop
        break

    stock_data = await fetch_stock_data(stock_symbol, start_date, end_date)
    save_to_excel(stock_data, stock_symbol, start_date, end_date)
    draw_candle_chart(pd.DataFrame(stock_data), stock_symbol)


asyncio.run(main())
