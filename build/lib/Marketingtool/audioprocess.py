# -*- coding: utf-8 -*-
import whisper
import os

class Audioprocess():
    def __init__(self):
        pass
    # transcribe speech
    def transcribeSpeech(self,videopath:str,model:str="base",language:str="English"):
        if os.path.exists(videopath)!=True:
            raise FileNotFoundError("File not found")
        model = whisper.load_model(model)
        audio = whisper.load_audio(videopath)
        audio = whisper.pad_or_trim(audio)
        # make log-Mel spectrogram and move to the same device as the model
        mel = whisper.log_mel_spectrogram(audio).to(model.device)

        # detect the spoken language
        _, probs = model.detect_language(mel)
        print(f"Detected language: {max(probs, key=probs.get)}")

        # decode the audio
        options = whisper.DecodingOptions()
        result = whisper.decode(model, mel, options)
        return result.text