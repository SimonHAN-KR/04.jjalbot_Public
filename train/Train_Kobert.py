import torch
import numpy as np
import pandas as pd
from torch import nn
import gluonnlp as nlp
import torch.optim as optim
from transformers import AdamW
import torch.nn.functional as F
from tqdm import tqdm, tqdm_notebook
from kobert.utils import get_tokenizer
from torch.utils.data import Dataset, DataLoader
from kobert.pytorch_kobert import get_pytorch_kobert_model
from sklearn.model_selection import StratifiedShuffleSplit
from transformers.optimization import get_cosine_schedule_with_warmup

# GPU 사용
use_cuda = True
device = torch.device("cuda:0")

# BERT 모델, Vocabulary 불러오기
bertmodel, vocab = get_pytorch_kobert_model()

# Load dataset
data = pd.read_excel('/content/drive/MyDrive/jjal_project/한국어_단발성_대화_데이터셋.xlsx')

# check null
data.isna().sum()

# label 비율별로 train/test split
sentence = pd.Series(data['Sentence'])
emotion = data['Emotion']

split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=1004)

for train_idx, test_idx in split.split(sentence, emotion):
    X_train = sentence[train_idx]
    X_test = sentence[test_idx]
    y_train = emotion[train_idx]
    y_test = emotion[test_idx]

# dataset으로 결합
dataset_train = []
for x, y in zip(X_train, y_train):
    data = []
    data.append(x)
    data.append(y)
    dataset_train.append(data)

dataset_test = []
for x, y in zip(X_test, y_test):
    data = []
    data.append(x)
    data.append(y)
    dataset_test.append(data)

emotion.max()

# 입력 데이터 생성
class BERTDataset(Dataset):
    def __init__(self, dataset, sent_idx, label_idx, bert_tokenizer, max_len,
                 pad, pair):
        transform = nlp.data.BERTSentenceTransform(
            bert_tokenizer, max_seq_length=max_len, pad=pad, pair=pair)

        self.sentences = [transform([i[sent_idx]]) for i in dataset]
        self.labels = [np.int32(i[label_idx]) for i in dataset]

    def __getitem__(self, i):
        return (self.sentences[i] + (self.labels[i], ))

    def __len__(self):
        return (len(self.labels))

# Check maxlen
sentence.str.len().max()

# Hyperparams
max_len = 64
batch_size = 64
warmup_ratio = 0.2
num_epochs = 100
max_grad_norm = 1
log_interval = 200
learning_rate = 4e-5

# Tokenizing
tokenizer = get_tokenizer()
tok = nlp.data.BERTSPTokenizer(tokenizer, vocab, lower=False)

data_train = BERTDataset(dataset_train, 0, 1, tok, max_len, True, False)
data_test = BERTDataset(dataset_test, 0, 1, tok, max_len, True, False)

train_dataloader = torch.utils.data.DataLoader(data_train, batch_size=batch_size, num_workers=4)
test_dataloader = torch.utils.data.DataLoader(data_test, batch_size=batch_size, num_workers=4)

# Training pretrained_KoBERT
class BERTClassifier(nn.Module):
    def __init__(self,
                 bert,
                 hidden_size = 768,
                 num_classes=7,
                 dr_rate=0.2,
                 params=None):
        super(BERTClassifier, self).__init__()
        self.bert = bert
        self.dr_rate = dr_rate
        self.classifier = nn.Sequential(
            nn.Linear(hidden_size, num_classes)  # Linear로만 구성해도 성능에 큰 차이를 보이지 않음(Dataset의 한계)
        if dr_rate:
            self.dropout = nn.Dropout(p=dr_rate)

    def gen_attention_mask(self, token_ids, valid_length):
        attention_mask = torch.zeros_like(token_ids)
        for i, v in enumerate(valid_length):
            attention_mask[i][:v] = 1
        return attention_mask.float()

    def forward(self, token_ids, valid_length, segment_ids):
        attention_mask = self.gen_attention_mask(token_ids, valid_length)
        
        _, pooler = self.bert(input_ids = token_ids, token_type_ids = segment_ids.long(), attention_mask = attention_mask.float().to(token_ids.device))
        if self.dr_rate:
            out = self.dropout(pooler)
        return self.classifier(out)

# Load BERT model
model = BERTClassifier(bertmodel).to(device)

# Setting optimizer and schedule
no_decay = ['bias', 'LayerNorm.weight']
optimizer_grouped_parameters = [
    {'params': [p for n, p in model.named_parameters() if not any(nd in n for nd in no_decay)], 'weight_decay': 0.01},
    {'params': [p for n, p in model.named_parameters() if any(nd in n for nd in no_decay)], 'weight_decay': 0.0}
]

optimizer = AdamW(optimizer_grouped_parameters, lr=learning_rate)
loss_fn = nn.CrossEntropyLoss()

t_total = len(train_dataloader) * num_epochs
warmup_step = int(t_total * warmup_ratio)

scheduler = get_cosine_schedule_with_warmup(optimizer, num_warmup_steps=warmup_step, num_training_steps=t_total)

# Calculating accuracy
def calc_accuracy(X,Y):
    max_vals, max_indices = torch.max(X, 1)
    train_acc = (max_indices == Y).sum().data.cpu()/max_indices.size()[0]
    return train_acc
    
train_dataloader

# Training classifier model
former_acc = 0.0
for e in range(num_epochs):
    train_acc = 0.0
    test_acc = 0.0
    model.train()
    for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(tqdm_notebook(train_dataloader)):
        optimizer.zero_grad()
        token_ids = token_ids.long().to(device)
        segment_ids = segment_ids.long().to(device)
        valid_length= valid_length
        label = label.long().to(device)
        out = model(token_ids, valid_length, segment_ids)
        loss = loss_fn(out, label)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_grad_norm)
        optimizer.step()
        scheduler.step()
        train_acc += calc_accuracy(out, label)
        if batch_id % log_interval == 0:
            print("epoch {} batch id {} loss {} train acc {}".format(e+1, batch_id+1, loss.data.cpu().numpy(), train_acc / (batch_id+1)))
    print("epoch {} train acc {}".format(e+1, train_acc / (batch_id+1)))
    
    model.eval()
    for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(tqdm_notebook(test_dataloader)):
        token_ids = token_ids.long().to(device)
        segment_ids = segment_ids.long().to(device)
        valid_length= valid_length
        label = label.long().to(device)
        out = model(token_ids, valid_length, segment_ids)
        test_acc += calc_accuracy(out, label)
    print("epoch {} test acc {}".format(e+1, test_acc / (batch_id+1)))

# Save model if current > former
    if test_acc / (batch_id+1) > former_acc:
        torch.save({
            'state' : model.state_dict(),
            'optimizer' : optimizer.state_dict(),
        }, '/content/drive/MyDrive/jjal_project/final_model{}.pt'.format(test_acc / (batch_id+1)))
        former_acc = test_acc / (batch_id+1)

# Predict function for test
def predict(predict_sentence):
    data = [predict_sentence, '0']
    dataset_another = [data]

    another_test = BERTDataset(dataset_another, 0, 1, tok, max_len, True, False)
    test_dataloader = torch.utils.data.DataLoader(another_test, batch_size=batch_size, num_workers=4)
    small_model.eval()

    for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(test_dataloader):
        token_ids = token_ids.long().to(device)
        segment_ids = segment_ids.long().to(device)

        valid_length= valid_length
        label = label.long().to(device)

        out = small_model(token_ids, valid_length, segment_ids)
        test_eval=[]
        for i in out:
            logits=i
            logits = logits.detach().cpu().numpy()

            for i in range(58):
                if np.argmax(logits) == i:
                    test_eval.append(le.inverse_transform(np.array([i])))
        print(">> 입력하신 내용에서 " + test_eval[0] + " 느껴집니다.")

'''
# test
while:
    sentence = input("하고싶은 말을 입력해주세요 : ")
    predict(sentence)
    print("\n")
'''