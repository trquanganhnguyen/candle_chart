# candle_chart

This project fetches stock data for a given symbol and date range, saves the data to an Excel file, and generates a candlestick chart. It uses asynchronous requests to fetch data efficiently from the API.

## Features

- Fetches stock data asynchronously for a given symbol and date range.
- Saves the fetched data to an Excel file.
- Generates a candlestick chart from the fetched data.

## Usage

### Run the script
```sh
python main.py
```

### Follow the prompts
```sh
Enter the stock symbol (3 alphabetic characters): 
Enter the start date (dd/mm/yyyy): 
Enter the end date (dd/mm/yyyy): 
```

### Output
- An Excel file with the stock data will be saved in folder 'Data'.
- A candlestick chart will be displayed


## Dependencies

- `aiohttp`: For making asynchronous HTTP requests.
- `pandas`: For handling data structures.
- `openpyxl`: For writing data to Excel files.
- `plotly`: For creating interactive charts.
