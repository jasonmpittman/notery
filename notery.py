#!/usr/bin/env python3

__author__ = "Jason M. Pittman"
__copyright__ = "Copyright 2022"
__credits__ = ["Jason M. Pittman"]
__license__ = "GPLv3"
__version__ = "0.1.0"
__maintainer__ = "Jason M. Pittman"
__email__ = "jason@jasonmpittman.com"
__status__ = "Development"

import re
import json
import gkeepapi
#import time
from os import path
import configparser
from datetime import datetime

class Notery:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')

        self.credentials = self.load_credentials()
        self.zettel_dir = config['DEFAULT']['ZettelDir']

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
            print("Searching for notes with tag " + tag)
            gnotes = keep.find(labels=[keep.findLabel(tag)])
            notes.append(gnotes)

            #print(gnotes)

            #for gnote in gnotes:
            #    #print(gnote)
            #    n = Note(gnote)
            #    print(n)
            #    notes.append(n)        

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

    def parse_id(self, note_id):
        match_id = re.search('\d{12}', note_id)
        id = match_id.group(0)

        return id

    def parse_title(self, note_title):
        match_title = re.search('\D+', note_title)
        title = match_title.group(0)

        return title.strip(' - ')

    def parse_tags(self, note_text):
        tags = re.findall('(#+[a-zA-Z0-9(_)]{1,})', note_text)
        
        return tags

    def write_zettel(self, notes):
        
        for note in notes:
            
            try:
                
                id = self.parse_id(note.title)
                title = self.parse_title(note.title)
                tags = self.parse_tags(note.text)
                
                zettel = path.join(self.zettel_dir, id)
                filename = '-' + title + '.md'

                f = open(zettel + filename, 'w+')

                # build the zettel header
                f.write('---\n')
                
                f.write('id: [[' + id + ']]' + '\n')
                f.write('title: [[' + title + ']]' + '\n')
                f.write('tags: ' + ' '.join(tags) + ' \n') 
                
                f.write('---\n\n')
                # end the zettel header

                # write the zettel body
                f.write(note.text)

                f.close()
            except Exception as e:
                print('Error writing note: ' + str(e))
            else:
                note.archived = True




def main():
    notery = Notery()
    keep = notery.login()
    
    notes = notery.get_notes(keep) #(keep.all())
    for note in notes:
        notery.write_zettel(note)
    
    keep.sync()

if __name__ == "__main__":
    main()