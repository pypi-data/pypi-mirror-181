import spacy
from exim import Exim


class BirdDetection:
    bird_list = []

    def find_bird_from_list(self,sentence):
        exim_ = Exim()
        all_birds_list = exim_.all_birds_list_padded
        bird_list = []
        sentence = " " + sentence + " "  # padding
        for bird in all_birds_list:
            if sentence.find(bird) > -1:
                bird_list.append(bird.strip())
        return bird_list


    def run_model(self, sentence):
        result_ = []
        nlp_ner = spacy.load("./model-best")
        doc = nlp_ner(sentence)
        for ent in doc.ents:
            result_.append(ent)
        return result_
