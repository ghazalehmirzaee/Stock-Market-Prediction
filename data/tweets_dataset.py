import torch
from torch.utils.data import Dataset
import csv

class TweetDataset(Dataset):
    def __init__(self, tweet_path, stock_path):
        self.tweet_headers, self.stock_headers = [], []
        self.tweets, self.stocks = [], {}
        
        with open(tweet_path, 'r') as file:
            reader = csv.DictReader(file)
            self.tweet_headers = reader.fieldnames
            
            for row in reader:
                self.tweets.append({'date': row['created_at'], 'text': row['text']})
            
        with open(stock_path, 'r') as file:
            reader = csv.DictReader(file)
            self.stock_headers = reader.fieldnames
            
            for row in reader:
                self.stocks.update({row['date']: row['price']})
        
        
            
    def __len__(self):
        return len(self.tweets)
    
    def __getitem__(self, index):
        tweet_data = self.tweets[index]
        stock_data = self.stocks.get(tweet_data['date'])
        
        return tweet_data['text'], 1 if (stock_data['open'] < stock_data['close']) else 0

if __name__ == "__main__":
    data = TweetDataset('cleaned-tweets.csv', 'cleaned-stocks.csv')
    
    print(len(data))