"""Module to fetch stock data from the SSI API and save it to an Excel file.

Using Async to start fetching all pages at once, or at least initiate multiple requests in parallel, 
reducing the total runtime."""

import os
from typing import List, Dict
import aiohttp

import pandas as pd


async def fetch_page_data(
    session: aiohttp.ClientSession, url: str, params: Dict[str, str]
) -> Dict:
    """Fetch data for a single page from the API.

    :param `aiohttp.ClientSession` session: The aiohttp session to use for the request.
    :param `str` url: The URL to send the GET request to.
    :param `Dict[str, str]` params: The parameters for the GET request.

    :return: The JSON response from the API.
    :rtype: Dict
    """
    try:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(f"Failed to retrieve data: {response.status}")
                return {}
    except Exception as e:
        print(f"Exception occurred: {e}")
        return {}


async def fetch_stock_data(
    stock_symbol: str, start_date: str, end_date: str, page_size: int = 50
) -> List[Dict]:
    """Fetch stock data for a given symbol and date range.

    :param str stock_symbol: The stock symbol to fetch data for.
    :param str start_date: The start date for the data in the format 'dd/mm/yyyy'.
    :param str end_date: The end date for the data in the format 'dd/mm/yyyy'.
    :param int page_size: The number of records to fetch per page. Default is 50.

    :return: A list of dictionaries containing the stock data.
    :rtype: List[Dict]
    """
    base_url = "https://iboard-api.ssi.com.vn/statistics/company/stock-price"
    all_data = []
    page = 1

    async with aiohttp.ClientSession() as session:
        while True:
            params = {
                "symbol": stock_symbol,
                "page": str(page),
                "pageSize": str(page_size),
                "fromDate": start_date,
                "toDate": end_date,
            }

            response_json = await fetch_page_data(session, base_url, params)
            if response_json and "data" in response_json:
                data = response_json["data"]
                if data:
                    all_data.extend(data)
                    if len(data) < page_size:  # No more data to fetch
                        break
                    page += 1
                else:
                    break
            else:
                break

    return all_data


def save_to_excel(
    data: List[Dict], stock_symbol: str, start_date: str, end_date: str
) -> None:
    """Save the stock data to an Excel file.

    :param List[Dict] data: The stock data fetched from API to save.
    :param str stock_symbol: The stock symbol for the filename.
    :param str start_date: The start date for the filename.
    :param str end_date: The end date for the filename.

    :return: None
    """
    if data:
        df = pd.DataFrame(data)
        # Format dates for the filename
        start_date_formatted = start_date.replace("/", "")
        end_date_formatted = end_date.replace("/", "")
        # Define the folder and create it if it doesn't exist
        folder_name = "Data"
        os.makedirs(folder_name, exist_ok=True)
        # Save the DataFrame to an Excel file
        filename = os.path.join(folder_name, f"{stock_symbol}_{start_date_formatted}_{end_date_formatted}.xlsx")
        df.to_excel(filename, index=False)
        print(f"Data saved to {filename} in folder {folder_name}.")
    else:
        print("No data to save.")
