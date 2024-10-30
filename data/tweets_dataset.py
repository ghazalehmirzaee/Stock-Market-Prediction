import torch
from torch.utils.data import Dataset, DataLoader
from tokenizers import Tokenizer
import csv

class TweetDataset(Dataset):
    def __init__(self, tweet_path, stock_path, tokenizer=None):
        self.tweet_headers, self.stock_headers = [], []
        self.tweets, self.stocks = [], {}
        tweet_valid_dates, self.valid_dates = [], []
        
        self.tokenizer = tokenizer
        
        with open(tweet_path, 'r') as file:
            reader = csv.DictReader(file)
            self.tweet_headers = reader.fieldnames
            
            for i in range(len(self.tweet_headers)): self.tweet_headers[i] = self.tweet_headers[i].lower()
            
            for row in reader:
                self.tweets.append({'date': row['date'], 'text': row['text'], 'stock': row['stock']})
                if [row['date'], row['stock']] not in tweet_valid_dates: tweet_valid_dates.append([row['date'], row['stock']])
            
        with open(stock_path, 'r') as file:
            reader = csv.DictReader(file)
            self.stock_headers = reader.fieldnames
            
            for i in range(len(self.stock_headers)): self.stock_headers[i] = self.stock_headers[i].lower()
            
            for row in reader:
                if row['stock'] not in self.stocks.keys(): self.stocks.update({row['stock']: []})
                self.stocks.get(row['stock']).append({'date': row['date'], 'open': row['open'], 'close': row['close']})
                if [row['date'], row['stock']] not in self.valid_dates and [row['date'], row['stock']] in tweet_valid_dates: 
                    self.valid_dates.append([row['date'], row['stock']])
            
    def __len__(self):
        return len(self.valid_dates)
    
    def __getitem__(self, index):
        date, stock = self.valid_dates[index]
        
        stock_data = [s for s in self.stocks[stock] if s['date'] == date][0]
        
        data = ""
        tweets = filter(lambda x: (x['date'] == date and x['stock'] == stock), self.tweets)
        for tweet in tweets:
            data += tweet['text'] + " "
        
        return (torch.tensor(self.tokenizer.encode(data).ids) if self.tokenizer is not None else data), (1 if (stock_data['open'] < stock_data['close']) else 0)

if __name__ == "__main__":
    tokenizer = Tokenizer.from_file("data/tokenizer_new_data.json")
    
    data = DataLoader(TweetDataset('data/new_data_tweets.csv', 'data/new_data_stocks.csv', tokenizer), 1, False)
    
    print(len(data))
    
    for i, (tweets, label) in enumerate(data):
        print(f"{i}: {tweets.shape}, {label}")