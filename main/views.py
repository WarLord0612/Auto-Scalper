from django.shortcuts import render

def stock_view(request):
    import yfinance as yf

    def calculate_rsi(prices, n=11):
        deltas = [prices[i+1] - prices[i] for i in range(len(prices)-1)]
        gains = [d if d > 0 else 0 for d in deltas]
        losses = [-d if d < 0 else 0 for d in deltas]
        avg_gain = sum(gains[:n]) / n
        avg_loss = sum(losses[:n]) / n
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    import csv
    
    nse_stock_codes = []

    # Open the CSV file
    with open("nse-indices-symbols.csv", 'r') as csvfile:
        # Create a CSV reader object
        reader = csv.reader(csvfile)
        
        # Read the header row
        header = next(reader)
        
        # Find the index of the column you want to read
        target_column_index = header.index('niftyall')
        
        # Iterate over the remaining rows and append the column value to the list
        for row in reader:
            column_value = row[target_column_index]
            nse_stock_codes.append(column_value)

    i=0
    d={}
    for stock_code in nse_stock_codes:
        try:
            stock_data = yf.download(stock_code, period='15d', interval='15m')
            close_prices = stock_data['Close'].dropna()
            rsi11 = calculate_rsi(close_prices[-11:])


            if rsi11 >80:
                d[i].append(stock_code)
                i=i+1
                if i==1:
                    break
        except:
            print(" ")

        
    return render(request,'home.html',{'d':d})


