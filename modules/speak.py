import pyttsx3

def Speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty("voices", voices[0].id)
    engine.setProperty("rate", 150)
    print(" ")
    print(f"Enco : {text}")
    engine.say(text=text)
    engine.runAndWait()
    #print(" ")
