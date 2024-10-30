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
    data = []
    headers = ['date', 'text', 'stock']
    
    with open(dataset_file, 'r') as file:
        reader = csv.DictReader(file)
        reader.fieldnames[0] = 'date'
        reader.fieldnames[1] = 'text'
        reader.fieldnames[2] = 'stock'
        
        for i, row in enumerate(reader):
            text = row['text']
            cleaned = clean_tweet_text(text)
            
            date = row['date'].split(' ')[0]
            
            data.append({'date': date, 'text': cleaned, 'stock': row['stock']})
        
    with open(save_file, 'w') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
        
def get_stocks(file, ticker, start, end):
    data = yf.download(ticker, start, end)
    data.to_csv(file)
    
def clean_stocks(dataset_file, save_file):
    headers, data = ['date', 'open', 'close', 'stock'], []
    
    with open(dataset_file, 'r') as file:
        reader = csv.DictReader(file)
        reader.fieldnames[0] = 'Date'
        reader.fieldnames[-1] = 'Stock'
        
        for i in range(len(reader.fieldnames)): reader.fieldnames[i] = reader.fieldnames[i].lower()
        
        reader.__next__()
        reader.__next__()
        for row in reader:
            data.append({
                'date': row['date'].split(' ')[0],
                'close': row['close'],
                'open': row['open'],
                'stock': row['stock']
            })
    
    with open(save_file, 'w') as file:
        writer = csv.DictWriter(file, headers)
        writer.writeheader()
        writer.writerows(data)
    
if __name__ == "__main__":
    #get_stocks('stocks-data.csv', '^GSPC', '2020-04-09', '2020-07-16')
    #clean_stocks('stocks-data.csv', 'cleaned-stocks.csv')
    clean_stocks('stock_yfinance_data.csv', 'new_data_stocks.csv')
    clean_tweets('stock_tweets.csv', 'new_data_tweets.csv')