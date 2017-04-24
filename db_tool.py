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
        cursor.execute('select game_id, review_id, text, score from svm_review order by review_id limit ? , ?;', (s, n))
        rows = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        return rows
