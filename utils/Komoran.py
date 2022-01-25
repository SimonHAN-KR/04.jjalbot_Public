from PyKomoran import Komoran, DEFAULT_MODEL

class Preprocess:
    def __init__(self, userdict = 'dic.user'):
        self.Komoran = Komoran(DEFAULT_MODEL['FULL'])
        self.Komoran.set_user_dic(userdict)

    def get_keyword(self, sentence):
        keyword_list = self.Komoran.get_list(sentence + ' ,라, *')
        return keyword_list