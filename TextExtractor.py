import csv

import nltk

from utils import Worker


class TextExtractor(Worker):

    def __init__(self, queue, cache_dict, stop_event, body_parts=[]):
        super().__init__(queue, cache_dict, stop_event)
        self.diseases, self.symptoms, self.drugs = self.load_data()
        self.vitals = ["temperature", "pulse", "blood pressure", "height", "weight"]
        self.cache_dict['diseases'] = []
        self.cache_dict['drugs'] = []
        self.cache_dict['symptoms'] = []
        self.cache_dict['vitals'] = []
        self.tokenizer = nltk.RegexpTokenizer(r'\w+')
        self.body_parts = body_parts

    def _step(self):
        try:
            message = self.queue.get()
            sentence = message[1]
            speaker = message[0]
            self.action(sentence, speaker)
        except Exception as e:
            print("GAL IS A FAILURE - ", e)

    def action(self, sentence, speaker):
        if speaker.lower() == "patient":
            self.patient_action(sentence)
        elif speaker.lower() == "doctor":
            self.doctor_action(sentence)

    def patient_action(self, sentence):
        tokenizer = nltk.RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(sentence)
        for t in tokens:
            t = t.lower()
            if t in self.symptoms and t not in self.cache_dict['symptoms']:
                self.cache_dict['symptoms'].append(t)

    def doctor_action(self, sentence):

        tokens = self.tokenizer.tokenize(sentence)
        for i, t in enumerate(tokens, start=1):
            t = t.lower()
            if is_negative(t):
                continue
            if t in self.diseases and t not in self.cache_dict['diseases']:
                self.cache_dict['diseases'].append(t)
            elif t in self.drugs and t not in self.cache_dict['drugs']:
                num = self.find_num(tokens)
                self.cache_dict['drugs'].append(t + " %s" % num)
            elif t in self.vitals and t not in self.cache_dict['vitals']:
                if tokens[i - 2] == 'high' or tokens[i - 2] == 'low':
                    t = tokens[i - 2] + " " + t
                num = self.find_num(tokens)
                self.cache_dict['vitals'].append(t + " %s" % num)

    def find_num(self, tokens):
        for t in tokens:
            if is_number(t):
                return t

    def find_negate(self, start, end):
        pass

    def load_data(self):
        with open('data.csv', encoding="utf8", errors='ignore') as f:
            # read the file as a dictionary for each row ({header : value})
            reader = csv.DictReader(f)
            data = {}
            for row in reader:
                for header, value in row.items():
                    try:
                        if value and len(value) > 1:
                            data[header].append(value.lower())
                    except KeyError:
                        data[header] = [value]

        # extract the variables you want
        return data['diseases'], data['symptoms'], data['drugs']


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def is_negative(token):
    if token.startswith("no") or token.endswith("nt"):
        return True
