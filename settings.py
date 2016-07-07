import json
import os

class Settings(object):
    def __init__(self):
        self.d = {}

    def save(self, fname:str):
        f = open(fname,'w')
        json.dump(self.d,f,indent=4 )
        f.close()

    def put(self, obj:object, cls:str, items:tuple):
        self.d[cls] = {}
        for item in items:
            self.d[cls][item] = getattr(obj,item)

    def get(self, obj:object, cls:str, items:tuple):
        dct = self.d[cls]
        for item in items :
            if item in dct.keys():
                setattr(obj,item,dct[item])



    def load(self, fname:str):
        if os.path.exists(fname):
            with open(fname, 'r') as f:
                self.d = json.load(f)
