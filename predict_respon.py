import os
import random
import json
import torch
import datetime
import req
from hear import Hear
from speak import Speak
from otak import NeuralNet
from NeuralNetwork import tas_kata, tokenize
from wiki import Wiki

try:
    open("PahamiData.pth")
except:
    Speak("Please wait sir, i will loaded my brain")
    os.system("python pahami.py")
    Speak("DONE, i have been loaded my brain")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
with open("memory.json", "r") as json_data:
    memories = json.load(json_data)

FILE = "PahamiData.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_kata = data["all_kata"]
tags = data["tags"]
model_state = data["model_state"]
responses = data["responses"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

def predict(sentence):
    sentence = tokenize(sentence)
    x = tas_kata(sentence, all_kata)
    x = x.reshape(1, x.shape[0])
    x = torch.from_numpy(x).to(device)

    output = model(x)

    _ , predicted = torch.max(output, dim=1)
    
    tag = tags[predicted.item()]
    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.3:
        for i in memories["intents"]:
            if tag == i["tag"]:
                sukses_predict_tag = i["tag"]
                sukses_predict_responses = i["responses"]
                break
            
        #response_index = tags.index(sukses_predict)
        #predicted_response = responses[response_index]
        return sukses_predict_tag, sukses_predict_responses

def find_matching_response(tex, all_responses):
    sukses_predict_tag, sukses_predict_responses = predict(tex)
    words = tex.lower().split()
    matching_responses = []
    for word in words:
        for response in all_responses:
            response_lower = response.lower()
            if word in response_lower:
                matching_responses.append(response)

    if matching_responses:
        return random.choice(matching_responses)
    else:
        return random.choice(all_responses)

def natural_res(senten=None, input_tag=None, output_tag=None):
    sukses_predict_tag, sukses_predict_responses = predict(senten)
    replied = []
    if senten is None and input_tag is not None and output_tag is not None:
        for i in memories["intents"]:
            if input_tag == i["tag"]:
                reply = random.choice(i["responses"])
                replied.append(reply)
                break
    if senten is not None and input_tag is None and output_tag is None:
        get_res = predict(senten)
        for i in memories["intents"]:
            if get_res == i["tag"]:
                reply = random.choice(i["responses"])
                replied.append(reply)
                break

    replied = replied[0].lower()
    if "morning" in replied or "afternoon" in replied or "evening" in replied:
        replied = replace_time(replied, waktu)

    return replied

def replace_time(reply, waktu):
    time_keywords = ["morning", "afternoon", "evening"]

    for keyword in time_keywords:
        if keyword in reply:
            reply = reply.replace(keyword, waktu)
            break
    return reply

while True:
    tex=input("input : ")
    tagnya , responnya = predict(tex)
    Speak(find_matching_response(tex, responnya))