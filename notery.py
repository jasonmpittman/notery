#!/usr/bin/env python3

__author__ = "Jason M. Pittman"
__copyright__ = "Copyright 2022"
__credits__ = ["Jason M. Pittman"]
__license__ = "GPLv3"
__version__ = "0.1.0"
__maintainer__ = "Jason M. Pittman"
__email__ = "jason@jasonmpittman.com"
__status__ = "Development"

import json
import gkeepapi
import time
import os
from datetime import datetime

from note import Note

class Notery:

    def __init__(self):
        self.credentials = self.load_credentials()

    def load_credentials(self):
        with open('credentials.json', 'r', encoding='utf-8') as f:
            credentials = json.load(f)
        
        return credentials

    def load_tags(self):
        with open('tags.json', 'r', encoding='utf-8') as f:
            t = json.load(f)
        
        tags = t['Tags']
        
        return tags

    def get_notes(self, keep):
        gnotes = []    
        notes = []

        t = self.load_tags()
        tags = [x.strip() for x in t[0].split(',')]

        for tag in tags:

            gnotes = keep.find(labels=[keep.findLabel(tag)])
            
            for gnote in gnotes:
                n = Note(gnote)
                notes.append(n)
                #print([note.title, note.text])
                #print("\n")            
        
        return notes

    def login(self):
        keep = gkeepapi.Keep()
        try:
            keep.login(self.credentials['UserName'], self.credentials['Password'])
        except:
            print("Enable login: https://accounts.google.com/b/0/DisplayUnlockCaptcha")
            raise
        finally:
            return keep


    def parse_text(self):
        #need to parse gkeep 'text' into note components
        #regex for hashtags
        #regex for id datestring

        pass

    def write_zettel(self, note):
        now = datetime.now()
        stamp = now.strftime("%Y%d%m%H%M")

        try:
            f = open(stamp + ".md", "w+")
            f.write('---\n')
            
            for k, v in self.__header.items():
                f.write(str(k) + ': ' + str(v) + '\n')
            
            f.write('---\n\n')

            fields = self.__body.split(',')
            for field in fields:
                f.write('## ' + field.strip(' ') + '\n\n')

            f.close()
        except Exception as e:
            print('Error writing note: ' + str(e))


def main():
    notery = Notery()
    keep = notery.login()
    
    notes = notery.get_notes(keep) #(keep.all())

    

if __name__ == "__main__":
    main()