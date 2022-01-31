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

class Notery:

    def __init__(self):
        self.credentials = self.load_credentials()

    def load_credentials(self):
        with open('credentials.json', 'r', encoding='utf-8') as f:
            credentials = json.load(f)
        
        return credentials

    def load_tags(self):
        with open('tags.json', 'r', encoding='utf-8') as f:
            tags = json.load(f)
        
        return tags

    def get_notes(self, keep):
        

        tags = self.load_tags()
        for tag in tags['Tags']:
            print(tag)

        notes = keep.find(labels=[keep.findLabel('reference')])
        
        for note in notes:
            print([note.title, note.text])
            print("\n")

    def login(self):
        keep = gkeepapi.Keep()
        try:
            keep.login(self.credentials['UserName'], self.credentials['Password'])
        except:
            print("Enable login: https://accounts.google.com/b/0/DisplayUnlockCaptcha")
            raise
        finally:
            return keep

    def write_zettel(self, note):
        pass


def main():
    notery = Notery()
    keep = notery.login()
    
    notery.get_notes(keep) #(keep.all())

if __name__ == "__main__":
    main()