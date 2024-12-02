import speech_recognition as sr

def Hear():
    while True:
        speech=sr.Recognizer()
        with sr.Microphone() as source:
            print("[Listening...]")
            speech.pause_threshold = 1
            audio = speech.listen(source, timeout=20)

        print("[Recognizing...]")
        try:
            query = speech.recognize_google(audio, language="en-US")
            print(f"You : {query}")
            return str(query).lower()
            break
        except:
            continue


    

