import os,sys,sqlite3

class DB:
    def __init__(self, config):
        self.db = config['DATABASE_URI']

    def update_review(self, game_id, review):
        conn = sqlite3.connect(self.db)
        conn.text_factory = str
        cursor = conn.cursor()
        cursor.execute('insert or replace into svm_review (game_id, text, score) \
                                                  values (?, ?, "0")', (game_id, review))
        rowcount = cursor.rowcount
        cursor.close()
        conn.commit()
        conn.close()
        return rowcount

    def update_review_score(self, review_id, score):
        conn = sqlite3.connect(self.db)
        conn.text_factory = str
        cursor = conn.cursor()
        cursor.execute('update svm_review set score = ? where review_id = ? ', (score, review_id))
        rowcount = cursor.rowcount
        cursor.close()
        conn.commit()
        conn.close()
        return rowcount

    def review_count(self):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute('select count(*) from svm_review')
        rows = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        return rows

    def fetch_review(self, s, n):
        conn = sqlite3.connect(self.db)
        conn.text_factory = str
        cursor = conn.cursor()
        cursor.execute('select review_id, game_id, text, score from svm_review order by review_id limit ? , ?;', (s, n))
        rows = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        return rows

    def fetch_review_useful(self, s, n):
        conn = sqlite3.connect(self.db)
        conn.text_factory = str
        cursor = conn.cursor()
        cursor.execute('select review_id, game_id, text, score from svm_review where score != 0 order by review_id limit ? , ?;', (s, n))
        rows = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        return rows

    def update_words(self, review_id, game_id, words, emotion_words):
        conn = sqlite3.connect(self.db)
        conn.text_factory = str
        cursor = conn.cursor()
        cursor.execute('insert or replace into svm_words (review_id, game_id, words, emotion_words) \
                                                  values (?, ?, ?, ?)', (review_id, game_id, words, emotion_words))
        rowcount = cursor.rowcount
        cursor.close()
        conn.commit()
        conn.close()
        return rowcount

    def fetch_words(self):
        conn = sqlite3.connect(self.db)
        conn.text_factory = str
        cursor = conn.cursor()
        cursor.execute('select review_id, game_id, words, emotion_words from svm_words order by review_id')
        rows = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        return rows

    def fetch_feature(self):
        conn = sqlite3.connect(self.db)
        conn.text_factory = str
        cursor = conn.cursor()
        cursor.execute('select review_id, game_id, feature, feature_score from svm_feature order by review_id')
        rows = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        return rows

    def update_feature(self, review_id, game_id, feature, feature_score):
        conn = sqlite3.connect(self.db)
        conn.text_factory = str
        cursor = conn.cursor()
        cursor.execute('insert or replace into svm_feature (review_id, game_id, feature, feature_score) \
                                                  values (?, ?, ?, ?)', (review_id, game_id, feature, feature_score))
        rowcount = cursor.rowcount
        cursor.close()
        conn.commit()
        conn.close()
        return rowcount
