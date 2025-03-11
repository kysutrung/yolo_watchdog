import speech_recognition as sr
from gtts import gTTS
import pygame
import os

def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        text_to_speech("Xin mời nói")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language="vi-VI")
            print("Nghe được: {}".format(text))
            return text
        except Exception as e:
            print(f"Không nhận dạng được giọng nói! Lỗi: {e}")
            return None

def process_command(text):
    if text.lower() == "tìm người":
        return "phát hiện người ở khu vực 2 4 6"
    else:
        return "He he he"

def text_to_speech(text):
    try:
        output = gTTS(text, lang="vi", slow=False)
        filename = "output.mp3"
        output.save(filename)
        
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.quit()
        
        os.remove(filename)
    except Exception as e:
        print(f"Lỗi khi phát âm thanh: {e}")

def voice_commandz():
    while True:
        text = speech_to_text()
        if text:
            response = process_command(text)
            text_to_speech(response)

def main():
    voice_commandz()

if __name__ == "__main__":
    main()
