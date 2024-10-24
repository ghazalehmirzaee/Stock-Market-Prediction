import csv
import yfinance as yf

def clean_tweet_text(text):
    text = text.replace('\n', ' ').replace('\t', ' ').replace('.', '').replace('?', '').replace('!', '')
    words = text.split(' ')
    
    cleaned = []
    for word in words:
        if '@' not in word and 'http' not in word: cleaned.append(word.lower())
    
    return ' '.join(cleaned)

def clean_tweets(dataset_file, save_file):
    data = {}
    headers = []
    
    with open(dataset_file, 'r') as file:
        reader = csv.DictReader(file)
        
        headers = reader.fieldnames
        
        for i, row in enumerate(reader):
            text = row['text']
            cleaned = clean_tweet_text(text)
            
            date = row['created_at'].split(' ')[0]
            
            data.update({date: (data.get(date) if date in data.keys() else '') + cleaned})
            
            if i % 2000 == 0: print(i)
    
    write = []
    for i, (date, text) in enumerate(zip(data.keys(), data.values())):
        write.append({'id': i, 'created_at': date, 'text': text})
        
    with open(save_file, 'w') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(write)
        
def get_stocks(file, ticker, start, end):
    data = yf.download(ticker, start, end)
    data.to_csv(file)
    
def clean_stocks(dataset_file, save_file):
    headers, data = [], []
    
    with open(dataset_file, 'r') as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames
        
        for row in reader:
            data.append({
                'Date': row['Date'].split(' ')[0], 
                'Adj Close': row['Adj Close'],
                'Close': row['Close'],
                'High': row['High'],
                'Low': row['Low'],
                'Open': row['Open'],
                'Volume': row['Volume']
            })
    
    with open(save_file, 'w') as file:
        writer = csv.DictWriter(file, headers)
        writer.writerows(data)
    
if __name__ == "__main__":
    get_stocks('stocks-data.csv', '^GSPC', '2020-04-09', '2020-07-16')
    clean_stocks('stocks-data.csv', 'cleaned-stocks.csv')
    clean_tweets('stock-market-tweets-data.csv', 'cleaned-tweets.csv')