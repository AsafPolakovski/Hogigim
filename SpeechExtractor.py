from utils import Worker
import speech_recognition as sr
import io
import time
import os


def transcribe_streaming_from_file(speech_file):
    """Transcribe the given audio file."""
    from google.cloud import speech_v1p1beta1 as speech
    from google.cloud.speech_v1p1beta1 import enums
    from google.cloud.speech_v1p1beta1 import types

    client = speech.SpeechClient()

    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code='en-US')

    response = client.recognize(config, audio)
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        # The first alternative is the most likely one for this portion.
        return result.alternatives[0].transcript


class SpeechExtractor(Worker):
    def __init__(self, queue, cache_dict, stop_event, speech_queue):
        self.speech_queue = speech_queue
        super().__init__(queue, cache_dict, stop_event)

    def _step(self):
        r = sr.Recognizer()
        mic = sr.Microphone(device_index=2)
        # print('Started')
        while True:
            with mic as source:
                # print('Mic is listening')
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
                self.speech_queue.put(audio)


class GoogleHandler(Worker):
    def __init__(self, queue, cache_dict, stop_event, speech_queue):
        self.speech_queue = speech_queue
        self.speaker = 'Doctor'
        super().__init__(queue, cache_dict, stop_event)

    def _step(self):
        try:
                audio = self.speech_queue.get()
                file_name = os.path.join('wav_files', str(time.time()) + '.wav')
                with open(file_name, "wb") as f:
                    # print('saving file')
                    f.write(audio.get_wav_data())
                if file_name is not None:
                    text = transcribe_streaming_from_file(file_name)
                    print("speech", self.speaker, text)
                    self.queue.put((self.speaker, text))
                    self.cache_dict["raw_text"] = "SPEAECHEXTRACTOR_{}|{}".format(self.speaker, text)
                    if self.speaker == 'Doctor':
                        self.speaker = 'Patient'
                    else:
                        self.speaker = 'Doctor'
        except Exception as e:
            self.queue.put(('exception', str(e)))
