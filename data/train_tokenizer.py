from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.pre_tokenizers import Whitespace

from tweets_dataset import TweetDataset

if __name__ == "__main__":
    data = TweetDataset('new_data_tweets.csv', 'new_data_stocks.csv')
    tokenizer = Tokenizer(BPE(unk_token="[UNK]"))
    tokenizer.pre_tokenizer = Whitespace()
    
    trainer = BpeTrainer(special_tokens=["[UNK]", "[CLS]", "[SEP]", "[PAD]", "[MASK]"])
    
    with open('tmp.txt', 'w') as file:
        for i, (tweet, label) in enumerate(data):
            if i % 500 == 0: print(i)
            file.write(tweet + '\n')
            
    tokenizer.train(['tmp.txt'], trainer)
    tokenizer.save("tokenizer_new_data.json")