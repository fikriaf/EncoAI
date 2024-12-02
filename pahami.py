import numpy as np
import json
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from NeuralNetwork import tas_kata, tokenize, stem
from otak import NeuralNet
from torch.nn.utils.rnn import pad_sequence

with open("memory.json", "r") as f:
    memori = json.load(f)

all_kata = []
tags = []
xy = []

hitung = 0
for i in memori["intents"]:
    tag = i["tag"]
    tags.append((tag))

    for p in i["patterns"]:
        r = i["responses"]
        print(p)
        print(r)
        w = tokenize(p)
        all_kata.extend(w)
        xy.append((w, tag, r))
        hitung+=1

print(hitung)

tanda_baca = [",", ".", "?", "/", "!"]
all_kata = [stem(w) for w in all_kata if w not in tanda_baca]
all_kata = sorted(set(all_kata))
tags = sorted(set(tags))

x_paham = []
y_paham = []

for (pattern_sentence, tag, responses) in xy:
    bag = tas_kata(pattern_sentence, all_kata)
    x_paham.append(torch.tensor(bag))

    label = tags.index(tag)
    y_paham.append(label)

padded_x_paham = pad_sequence(x_paham, batch_first=True, padding_value=0)

x_paham = padded_x_paham.numpy()
y_paham = np.array(y_paham)

num_epochs = 1000
batch_size = 8
learning_rate = 0.001
input_size = len(x_paham[0])
hidden_size = 8
output_size = len(tags)

print("[Memahami memory...]")

class ChatDataSet(Dataset):
    def __init__(self):
        self.n_samples = len(x_paham)
        self.x_data = torch.from_numpy(x_paham)
        self.y_data = torch.from_numpy(y_paham)
        self.responses = [responses for _, _, responses in xy]

    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index], self.responses[index]

    def __len__(self):
        return self.n_samples

def collate_fn(batch):
    sequences = [item[0] for item in batch]
    labels = [item[1] for item in batch]
    responses = [item[2] for item in batch]

    labels_tensor = torch.tensor(labels, dtype=torch.long)

    max_response_length = max(len(response) for response in responses)
    padded_responses = torch.zeros((len(responses), max_response_length), dtype=torch.long)
    for i, response in enumerate(responses):
        encoded_response = [response_to_index[r] for r in response]
        padded_responses[i, :len(encoded_response)] = torch.tensor(encoded_response, dtype=torch.long)

    return torch.stack(sequences, dim=0), labels_tensor, padded_responses


dataset = ChatDataSet()

response_to_index = {response: idx for idx, response in enumerate(set(response for responses in dataset.responses for response in responses))}
responses_encoded = [[response_to_index[response] for response in responses] for responses in dataset.responses]
responses_tensor = [torch.tensor(responses, dtype=torch.long) for responses in responses_encoded]

load_paham = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True, num_workers=0, collate_fn=collate_fn)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = NeuralNet(input_size, hidden_size, output_size).to(device=device)
kriteria = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

for epoch in range(num_epochs):
    for (words, labels, responses) in load_paham:
        words = words.to(device)
        labels = labels.to(device)
        responses = responses.to(device)
        outputs = model(words)
        loss = kriteria(outputs, labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    if (epoch + 1) % 100 == 0:
        print(f"Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}")

print(f"Final Loss: {loss.item():.4f}")

data = {
    "model_state": model.state_dict(),
    "input_size": input_size,
    "hidden_size": hidden_size,
    "output_size": output_size,
    "all_kata": all_kata,
    "tags": tags,
    "responses": [response for _, _, response in xy]
}

FILE = "PahamiData.pth"
torch.save(data, FILE)

print(f"[Sukses memahami 'memory.json' --{FILE}--]")
