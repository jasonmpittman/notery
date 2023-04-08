#!/usr/bin/env python3

__author__ = "Jason M. Pittman"
__copyright__ = "Copyright 2023"
__credits__ = ["Jason M. Pittman"]
__license__ = "GPLv3"
__version__ = "0.2.0"
__maintainer__ = "Jason M. Pittman"
__email__ = "jason@jasonmpittman.com"
__status__ = "Development"

import re
import json
import gkeepapi
import argparse
import os
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

        tags = self.load_tags() 

        for tag in tags:
            print("Searching for notes with tag " + tag)
            gnotes = keep.find(labels=[keep.findLabel(tag)], archived=False)
            notes.append(gnotes)       

        return notes

    def authenticate(self):
        keep = gkeepapi.Keep()

        try:
            keep.login(self.credentials['UserName'], self.credentials['Password'])
        except gkeepapi.exception.LoginException as ex:
            raise Exception("https://myaccount.google.com/apppasswords")
        finally:
            return keep

    def parse_id(self, note_id):
        match_id = re.search('\d{12}', note_id)
        
        try:
            id = match_id.group(0)
            return id
        except AttributeError:
            return "EMPTY ID"

    def parse_title(self, note_title):
        match_title = re.search('\D+', note_title)
        
        try:
            title = match_title.group(0)
            return title.strip(' - ')
        except AttributeError:
            return "EMPTY TITLE"

    def parse_tags(self, note_text):
        tags = re.findall('(#+[a-zA-Z0-9(_)]{1,})', note_text)
        
        return tags

    def convert_date(self, input_date):
        converted_date = datetime.strftime(input_date, '%Y%m%d%H%M%S%f')[:-3]

        return converted_date

    def clean_body_text(self, text):
        cleaned_text = re.sub('[#]\w*', '', text)

        return cleaned_text

    def write_zettel(self, notes):

        for note in notes:

            # build the core parts of the zettel    
            id = self.parse_id(note.title)
            title = self.parse_title(note.title)
            tags = self.parse_tags(note.text)
            dtstamp = str(self.convert_date(note.timestamps.created))
                
            #check for 'data' directory
            current_path = os.getcwd()
            zettel_path = os.path.join(current_path, self.zettel_dir)

            if not os.path.exists(zettel_path):
                try:
                    os.mkdir(zettel_path)
                except OSError:
                    raise OSError.strerror
                else:
                    print('Created zettel directory successfully')

            zettel = os.path.join(zettel_path, id)
            filename = '-' + title + '.md'
            
            #check if file exists and don't overwrite
            if not os.path.isfile(zettel + filename):
                print('Writing {}: '.format(zettel + filename))
                try:
                    f = open(zettel + filename, 'w+')

                    f.write('created: ' + dtstamp + '\n') 
                    f.write('modified: ' + dtstamp + '\n') 
                    f.write('tags: ' + ' '.join(tags) + '\n')                
                    f.write('title: ' + id + ' ' + title + '\n')
                    f.write('type: text/vnd.tiddlywiki' + '\n')

                    f.write(self.clean_body_text(note.text))

                    f.close()
                except Exception as e:
                    print('Error writing note: ' + str(e))
                else:
                    print('Archiving this note in Keep')
                    note.archived = True
            else:
                print('{} exists...skipping '.format(zettel + filename))




def main():

    notery = Notery()
    keep = notery.authenticate()

    parser = argparse.ArgumentParser(description="Utility to convert Google Keep notes into local zettels")
    parser.add_argument('-t', '--test', help="test the connection to your Keep", action="store_true")
    parser.add_argument('-l', '--list', help="list the Keep notes matching our tags", action="store_true")
    parser.add_argument('-w', '--write', help="write Keep notes to local tiddlers", action="store_true")

    args = parser.parse_args()

    if args.test:
        print(keep)

    if args.list:
        notes = notery.get_notes(keep)
        for note in notes:
            for n in note:
                print(n)
    
    if args.write:        
        notes = notery.get_notes(keep)

        for note in notes:
            notery.write_zettel(note)
            
    
    keep.sync()

if __name__ == "__main__":
    main()