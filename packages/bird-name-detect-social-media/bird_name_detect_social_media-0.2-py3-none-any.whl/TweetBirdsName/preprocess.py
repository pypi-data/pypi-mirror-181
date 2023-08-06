from exim import Exim

import re
import demoji
import preprocessor as p
import spacy
nlp = spacy.load("en_core_web_sm")
p.set_options(p.OPT.EMOJI, p.OPT.MENTION, p.OPT.URL, p.OPT.SMILEY, p.OPT.NUMBER, p.OPT.HASHTAG)


class UserSentence:
    text = ""
    preprocessed_text = ""
    spelling_corrections = {"grey": "gray", "pegion": "pigeon", "brested": "breasted", "serpant": "serpent",
                            "avedavat": "avadavat", "open billed stork": "asian openbill",
                            "secretary bird": "Secretarybird", "dollar bird": "dollarbird", "silver bill": "silverbill",
                            "eyes": "eye"}

    def get_bird_name_from_hashtag_4levels(self, hashtag_, all_birds_list):
        hashtag_ = hashtag_.lower()
        special_cases = {"greateradjutantstork": "greateradjutant"}

        for key in special_cases:
            if hashtag_ == key: hashtag_ = special_cases[key]

        rel_birdnames = []
        for bird in all_birds_list:
            if bird[-2:] == hashtag_[-2:] and hashtag_[:2] == bird[:2]:
                rel_birdnames.append(bird)

        if len(rel_birdnames) > 0:
            if hashtag_ in rel_birdnames:
                return hashtag_
            segments = [0, 1, 2, 3]
            m_ = 2
            while m_ < len(hashtag_) - 2:
                segments[0] = hashtag_[:m_]
                n_ = 0
                while n_ < len(hashtag_[m_:]):
                    segments[1] = hashtag_[m_:][:n_]
                    part3 = hashtag_[m_:][n_:]
                    o_ = 0
                    while o_ < len(hashtag_[m_:][n_:]):
                        segments[2] = hashtag_[m_:][n_:][:o_]
                        p_ = 0
                        while p_ < len(hashtag_[m_:][n_:][o_:]):
                            segments[3] = hashtag_[m_:][n_:][o_:][:p_]
                            part4 = hashtag_[m_:][n_:][o_:][p_:]
                            prob_birdname = segments[0] + " " + segments[1] + " " + segments[2] + " " + segments[3] + " " + part4
                            prob_birdname = re.sub(r' +', ' ', prob_birdname)
                            if prob_birdname in rel_birdnames:
                                return prob_birdname
                            p_ += 1
                        o_ += 1
                    n_ += 1
                m_ += 1
        return None

    def remove_emojis(self, sentence):
        emojis = demoji.findall(sentence)
        for item in emojis:
            sentence = sentence.replace(item, " " + emojis[item] + " ")
        return sentence

    def replace_underscores(self, sentence):
        sentence = sentence.lower()
        sentence = sentence.replace("_", " ")
        return sentence

    def try_replacing_hashtags_mit_birdname(self, text, all_birds_list):
        status = False
        hashtags = re.findall(r"#(\w+)", text)
        for hashtag in hashtags:
            segmented_ = self.get_bird_name_from_hashtag_4levels(hashtag, all_birds_list)
            if segmented_ is not None: text = text.replace("#" + hashtag, segmented_)
        return text

    def basic_preprocess(self, sentence):
        sentence = p.clean(sentence)
        if sentence[:2] == "b'":
            sentence = sentence[1:]
        sentence = re.sub(r'[^\w\s]', ' ', sentence)
        sentence = re.sub(r' +', ' ', sentence)
        sentence = sentence.strip()
        for key in self.spelling_corrections:
            if sentence.find(key) > -1:
                sentence = sentence.replace(key, self.spelling_corrections[key])
        return sentence

    def plural_nn_to_singular(self, sentence, birdnames_words):
        doc = nlp(sentence)
        for token in doc:
            if token.pos_ == "NOUN":
                if token.text[-1:] == "s" and token.text not in birdnames_words:
                    sentence = sentence.replace(token.text, token.text[:-1])
        return sentence

    def preprocess(self, text):
        exim = Exim()
        text = self.remove_emojis(text)  # Removes Emojis
        text = self.replace_underscores(text)  # Replaces underscores
        text = self.try_replacing_hashtags_mit_birdname(text, exim.all_birds_list)
        text = self.basic_preprocess(text)
        text = self.plural_nn_to_singular(text, exim.birdnames_words)
        return text

    def __init__(self, text_):
        self.text = text_
        self.preprocessed_text = self.preprocess(text_)