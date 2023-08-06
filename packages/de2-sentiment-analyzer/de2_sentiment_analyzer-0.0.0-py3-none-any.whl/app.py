import os
from transformers import AutoTokenizer
import csv
from scipy.special import softmax
import numpy as np
from transformers import AutoModelForSequenceClassification


class NLPModelPipeline:
    def __init__(self, model_name='cardiffnlp/twitter-roberta-base-sentiment',
                 base_path="de2_sentiment_analyzer/config_store"):
        self.base_path = base_path
        self.model_name = model_name
        self.config_store_dir = {"tokenizer_files": f"{self.base_path}/tokenizer",
                                 "label_files": f"{self.base_path}/mapping.txt",
                                 "model_files": f"{self.base_path}/model"
                                 }
        self.labels = self.load_mapping()
        print("labels loaded")
        self.tokenizer = self.load_tokenizer()
        print("tokenizer loaded")
        self.model = self.load_model()
        print("model loaded")

    def input_preprocess(self, input_text):
        new_text = []
        for t in input_text.split(" "):
            t = '@user' if t.startswith('@') and len(t) > 1 else t
            t = 'http' if t.startswith('http') else t
            new_text.append(t)
        return " ".join(new_text)

    def load_tokenizer(self):
        if os.path.exists(self.config_store_dir['tokenizer_files']):
            return AutoTokenizer.from_pretrained(self.config_store_dir['tokenizer_files'])
        else:
            raise FileNotFoundError("There is not pretrained file here")

    def load_model(self):
        if os.path.exists(self.config_store_dir['model_files']):
            return AutoModelForSequenceClassification.from_pretrained(self.config_store_dir['model_files'])
        else:
            raise FileNotFoundError("There is not pretrained file here")

    def load_mapping(self):
        with open(self.config_store_dir['label_files']) as labels_file:
            html = labels_file.read().split("\n")
            csvreader = csv.reader(html, delimiter='\t')
        return [row[1] for row in csvreader if len(row) > 1]

    def process_scores(self, raw_score, labels):
        max_score = 0.
        label = None
        ranking = np.argsort(raw_score)
        ranking = ranking[::-1]
        for i in range(raw_score.shape[0]):
            score = np.round(float(raw_score[ranking[i]]), 4)
            if score > max_score:
                label = labels[ranking[i]]
                max_score = raw_score[ranking[i]]
                print(f'Max prob for label - {label} is : {max_score}')
        if not label:
            raise Exception("Prob cannot be 0")
        return label

    def run(self, input_text):
        text = self.input_preprocess(input_text)
        encoded_input = self.tokenizer(text, return_tensors='pt')
        output = self.model(**encoded_input)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)

        return self.process_scores(scores, self.labels)


if __name__ == '__main__':
    sample_texts = ["Good night 😊", "This restaurant is so bad", "This is a nice place", "I cannot work here"]
    pl_obj = NLPModelPipeline(base_path="config_store")
    for sample_text in sample_texts:
        print(f"Response is : {pl_obj.run(sample_text)}")
