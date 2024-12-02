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

now = datetime.datetime.now()
if now.hour > 0 and now.hour < 11:
    waktu = "morning"
elif now.hour >= 11 and now.hour < 14:
    waktu = "afternoon"
elif now.hour >= 14 and now.hour < 24:
    waktu = "evening"

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

def natural_res(tex, all_responses):
    words = tex.lower().split()
    matching_responses = []
    for word in words:
        for response in all_responses:
            response_lower = response.lower()
            if word in response_lower:
                matching_responses.append(response)

    if matching_responses:
        replied = random.choice(matching_responses).lower()
        if "morning" in replied or "afternoon" in replied or "evening" in replied:
            replied = replace_time(replied, waktu)

    else:
        replied = random.choice(all_responses).lower()
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
#-------------------------
Nama = "Enco"
#-------------------------
def Main():
    #sentence = Hear()
    sentence = input("You : ")

    sukses_predict_tag, sukses_predict_responses = predict(sentence)
    _, get_need = predict("I need more time")
    need = natural_res("karepmu", get_need)

    if "wikipedia" in sukses_predict_tag:
        Speak(natural_res(sentence, sukses_predict_responses))
        hasil_wiki = Wiki(sentence)
        Speak(need)
    elif "pray_schedule" in sukses_predict_tag:
        Speak(natural_res(sentence, sukses_predict_responses))
        req.JadwalSalat()
        Speak(need)
    elif "news" in sukses_predict_tag:
        Speak(natural_res(sentence, sukses_predict_responses))
        req.News()
        Speak(need)
    elif "play music" in sukses_predict_tag:
        Speak(natural_res(sentence, sukses_predict_responses))
        req.Music()
        Speak(need)
    elif "next music" in sukses_predict_tag:
        Speak(natural_res(sentence, sukses_predict_responses))
        req.NextMusic()
        Speak(need)
    elif "goodbye" in sukses_predict_tag:
        Speak(natural_res(sentence, sukses_predict_responses))
        exit()
    else:
        Speak(natural_res(sentence, sukses_predict_responses))
        

while True:
    Main()