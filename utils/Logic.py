from DAO import *
from komoran import *
from collections import Counter
import random
import sys
sys.path.append('../models')
from Kobert_model import *

class Logic:
    def __init__(self):
        self.komo = Preprocess()
        self.dao = JjalDao() 
        self.emo = Predict()

    def komoran(self, word):
        self.pairs = []
        self.word = word
        self.pairs = self.komo.get_keyword(self.word) 

    def Kobert(self, word):
        self.word = word
        self.em_result = ''
        self.em_result = self.emo.predict(word)
        return self.em_result

    def dao_split(self):
        self.ob_result = []
        self.ac_result = []
        self.em_result = []
        self.word_ob = ()
        self.word_ac = ()
        self.word_em = ()
        for i in self.pairs:
            pos = i.get_second()
            if pos == 'NNP' or pos == 'NNG':
                self.word_ob = self.dao.sel_object(i.get_first())
                if self.word_ob != ():
                    for i in self.word_ob[0][0].split(','):
                        self.ob_result.append(i)
            elif i.get_second() in ['NNP', 'NP', 'NNG', 'VV', 'VX', 'VA', 'XR', 'MAG']:
                self.word_ac = self.dao.sel_action(i.get_first())
                if self.word_ac != ():
                    for i in self.word_ac[0][0].split(','):
                        self.ac_result.append(i)
        if len(self.ob_result) ==0 and len(self.ac_result) == 0:
            self.em_result = self.Kobert(self.word)
            self.word_em = self.dao.sel_emotion(self.em_result)
            self.word_em = self.word_em.split(',')
            self.em_result = list(map(str, self.word_em))

    # object, action dictionary count up
    def mal_logic(self, word):
        self.word = word.replace('.말 ', '')
        self.word_mal = self.word[0] + self.word[1]
        self.mal_result = []
        self.final = []
        self.word_mal = self.dao.sel_mal(self.word_mal)
        self.word_mal = self.word_mal.split(',')
        self.mal_result = list(map(str, self.word_mal))
        self.max_len = len(self.word) - 3
        self.tmp_result = []
        for i in self.mal_result:
            tmp = self.dao.sel_main(i).split(',')
            if int(tmp[3]) < self.max_len:
                pass
            else:
                self.tmp_result.append(tmp)
        # maxlen를 충족하지 못하는 이미지는 삭제
        for i in self.tmp_result:
            if int(i[3]) < self.max_len:
                serf.mal_result.remove(i)
        # 결과값 반환
        if len(self.tmp_result) > 3:
            tmp = random.sample(self.tmp_result, 3)
            for i in tmp: self.final.append(i)
        else:
            self.final = self.tmp_result
        return self.final
    
    def result(self):
        self.final = []
        self.semifinal = []
        # action count_dict 구성
        self.ob_count = Counter(self.ob_result)
        self.ac_count = Counter(self.ac_result)
        self.em_count = self.em_result
        self.ob2_count_set = set()
        self.ob1_count_set = set()
        self.ac2_count_set = set()
        self.ac1_count_set = set()

        # list : count object, action
        for k, v in self.ob_count.items():
            if v >= 2: self.ob2_count_set.add(k)
            else: self.ob1_count_set.add(k)

        for k, v in self.ac_count.items():
            if v >= 2: self.ac2_count_set.add(k)
            else: self.ac1_count_set.add(k)

        # object >= 2
        first_priority = self.ob2_count_set & self.ac2_count_set
        if len(first_priority) > 3:
            tmp = random.sample(first_priority, 3)
            for i in tmp: self.final.append(i)
        else:
            for i in first_priority: self.final.append(i)
            second_priority = self.ob2_count_set & self.ac1_count_set
            if len(self.final) + len(second_priority) > 3:
                tmp = random.sample(second_priority, 3 - len(self.final))
                for i in tmp: self.final.append(i)
            else:
                for i in second_priority: self.final.append(i)
                third_priority = self.ob2_count_set - first_priority - second_priority
                if len(self.final) + len(third_priority) > 3:
                    tmp = random.sample(third_priority, 3 - len(self.final))
                    for i in tmp: self.final.append(i)
                else:
                    for i in third_priority: self.final.append(i)
                    # ob가 1개인 경우
                    fourth_priority = self.ob1_count_set & self.ac2_count_set
                    if len(self.final) + len(fourth_priority) > 3:
                        tmp = random.sample(fourth_priority, 3 - len(self.final))
                        for i in tmp: self.final.append(i)
                    else:
                        for i in fourth_priority: self.final.append(i)
                        fifth_priority = self.ob1_count_set & self.ac1_count_set
                        if len(self.final) + len(fifth_priority) > 3:
                            tmp = random.sample(fifth_priority, 3 - len(self.final))
                            for i in tmp: self.final.append(i)
                        else:
                            for i in fifth_priority: self.final.append(i)
                            sixth_priority = self.ob1_count_set - fourth_priority - fifth_priority
                            if len(self.final) + len(sixth_priority) > 3:
                                tmp = random.sample(sixth_priority, 3 - len(self.final))
                                for i in tmp: self.final.append(i)
                            else:
                                for i in sixth_priority: self.final.append(i)
                                seventh_priority = self.ac2_count_set - first_priority - fourth_priority
                                if len(self.final) + len(seventh_priority) > 3:
                                    tmp = random.sample(seventh_priority, 3 - len(self.final))
                                    for i in tmp: self.final.append(i)
                                else:
                                    for i in seventh_priority: self.final.append(i)
                                    # ob가 없는경우
                                    eighth_priority = self.ac1_count_set - second_priority - fifth_priority
                                    if len(self.final) + len(eighth_priority) > 3:
                                        tmp = random.sample(eighth_priority, 3 - len(self.final))
                                        for i in tmp: self.final.append(i)
                                    else:
                                        for i in eighth_priority: self.final.append(i)
                                        if len(self.final) == 0:
                                            if len(self.em_count) > 3:
                                                tmp = random.sample(self.em_count, 3)
                                                for i in tmp: self.final.append(i)
                                            else:
                                                self.final = self.em_count
        return self.final