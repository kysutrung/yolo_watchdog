import speech_recognition as sr
from gtts import gTTS
import playsound
import os

def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Nói đê bạn êii")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language="vi-VI")
            print("Nghe được: {}".format(text))
            return text
        except:
            print("Không nhận dạng được giọng nói!")
            return None

def process_command(text):
    if text == "Hello":
        return "Chào bạn"
    else:
        return "He he he"

def text_to_speech(text):
    output = gTTS(text, lang="vi", slow=False)
    output.save("output.mp3")
    playsound.playsound('output.mp3', True)
    os.remove("output.mp3")

def main():
    while True:
        text = speech_to_text()
        if text:
            response = process_command(text)
            text_to_speech(response)

if __name__ == "__main__":
    main()
