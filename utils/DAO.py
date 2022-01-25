import pymysql
from sqlalchemy import text, create_engine

class JjalDao:
    def connect(self):
        return pymysql.connect(host='0.0.0.0', port=3306, user='bigdata',
                              password='123',db='chat',charset='utf8')

    def sel_action(self,word):
        conn = self.connect()
        sql = "select idx from action where 단어=%s"
        cursor = conn.cursor()
        cursor.execute(sql,word)
        result = cursor.fetchall()
        conn.close()
        return result
        
    def sel_emotion(self,word):
        conn = self.connect()
        sql = "select idx from emotion where 단어=%s"
        cursor = conn.cursor()
        cursor.execute(sql,word)
        result = cursor.fetchall()
        conn.close()
        return result[0][0]
        
    def sel_object(self,word):
        conn = self.connect()
        sql = "select idx from object where 단어=%s"
        cursor = conn.cursor()
        cursor.execute(sql,word)
        result = cursor.fetchall()
        conn.close()
        return result

    def sel_mal(self,word):
        conn = self.connect()
        sql = "select idx from mal where 단어=%s"
        cursor = conn.cursor()
        cursor.execute(sql,word)
        result = cursor.fetchall()
        conn.close()
        return result[0][0]    

    def sel_main(self,idx):
        conn = self.connect()
        sql = "select URL from mal_main where IDX=%s"
        cursor = conn.cursor()
        cursor.execute(sql,idx)
        result = cursor.fetchall()
        conn.close()
        return result[0][0]
