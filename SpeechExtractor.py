from utils import Worker
import speech_recognition as sr
import io


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
        return result.alternatives[0].transcript


class SpeechExtractor(Worker):
    def _step(self):
        try:
            r = sr.Recognizer()
            r.pause_threshold = 0.5
            mic = sr.Microphone(device_index=2)
            speaker = 'Doctor'
            # print('Started')
            while True:
                with mic as source:
                    # print('Mic is listening')
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source)
                    with open("microphone-results.wav", "wb") as f:
                        # print('saving file')
                        f.write(audio.get_wav_data())
                # print('transcribing')
                text = transcribe_streaming_from_file(r"microphone-results.wav")
                self.queue.put((speaker, text))
                if speaker == 'Doctor':
                    speaker = 'Patient'
                else:
                    speaker = 'Doctor'
        except Exception as e:
            self.queue.put(('exception', e.message))


        #self.queue.put("Send Message to Text Extractor")
        #self.cache_dict["raw_text"] = "GAL BRAUNNN" + str(time.time())
