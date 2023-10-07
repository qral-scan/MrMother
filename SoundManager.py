import sounddevice as sd
import torch
import random
from Texts import default_sound_messages, nothing_to_send_sound_messages
from Config import sound_is_on
from threading import Thread


class SoundManager:
    def __init__(self):
        language = 'ru'
        model_id = 'v4_ru'
        device = torch.device('cpu')

        self.speaker = 'baya'
        self.sample_rate = 48000
        self.model, _ = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                       model='silero_tts',
                                       language=language,
                                       speaker=model_id)
        self.model.to(device)
        self.text = None
        self.audio = None
        self.thread = None

    def notify(self, found: bool = None, text: str = None):
        def proceed():
            if sound_is_on:
                messages = default_sound_messages if found else nothing_to_send_sound_messages
                self.text = random.choice(messages)
                self.audio = self.model.apply_tts(text=text if text else self.text,
                                                  speaker=self.speaker,
                                                  sample_rate=self.sample_rate,
                                                  put_accent=True,
                                                  put_yo=True)
                sd.play(self.audio, self.sample_rate)
                sd.wait()
                sd.stop()

        self.thread = Thread(target=proceed)
        self.thread.start()
