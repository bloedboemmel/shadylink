
import sketchify
import sketchy_data
import random
import sqlite3

class URLStoreModel():
    
        def __init__(self):
    
            self.db = sqlite3.connect("urls.db", check_same_thread=False)
            try:
                self.db.execute("SELECT * FROM urls")
            except sqlite3.OperationalError:
                self.create_table("urls", ("long_url", "sketchy_url"))
                self.initial_setup()
            self.initial_setup()

        def create_table(self, tablename, tableheaders):
            try:
                self.db.execute("CREATE TABLE %s%s" % (tablename, tuple(tableheaders)))
                self.db.commit()
                return
            except sqlite3.OperationalError:
                return
        def initial_setup(self):
            if not self.get_sketchy_url(random.choice(sketchy_data.SAMPLE_LONG_URLS)):
                for sample_long_url in sketchy_data.SAMPLE_LONG_URLS:
                    self.add(sample_long_url)
    
        def add(self, long_url):
            sketchy_url = sketchify.generate_sketchy_url()
            self.set_url(long_url, sketchy_url)
    
        def set_url(self, long_url, sketchy_url):
    
            self.db.execute("INSERT INTO urls (long_url, sketchy_url) VALUES (?, ?)", (long_url, sketchy_url))
            self.db.commit()
    
            #print("Setting " + long_url + " -> " + sketchy_url)
    
        def get_long_url(self, sketchy_url):
    
            cursor = self.db.execute("SELECT long_url FROM urls WHERE sketchy_url = ?", (sketchy_url,))
            result = cursor.fetchone()
    
            # None if we don't have this URL already
            if not result:
                #print("Getting: " + sketchy_url + " -> " + str(result))
                return None
    
            long_url = result[0]
            return long_url
    
        def get_sketchy_url(self, long_url):
    
            cursor = self.db.execute("SELECT sketchy_url FROM urls WHERE long_url = ?", (long_url,))
            result = cursor.fetchone()
    
            #print(result)
            if not result:
                #print("Getting: " + long_url + " -> None")
                return None
    
            sketchy_url = result[0]
    
            return sketchy_url

if __name__ == "__main__":
    URLStoreModel().initial_setup()