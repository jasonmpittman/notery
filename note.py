

__author__ = "Jason M. Pittman"
__copyright__ = "Copyright 2022"
__credits__ = ["Jason M. Pittman"]
__license__ = "GPLv3"
__version__ = "0.1.0"
__maintainer__ = "Jason M. Pittman"
__email__ = "jason@jasonmpittman.com"
__status__ = "Development"


import time
import os
import configparser
from datetime import datetime


class Note:

    __header = {
        'id': '',
        'title': '',
        'body': '',
        'tags': []
    }

    def __init__(self, n):
        self.__header['title'] = n.Title # i think we need to parse the short sentence from n.Text
        self.__header['body'] = n.Text
        self.__header['id'] = n.Title #the title in gkeep is the date based id
        self.__header['tags'] = n.Labels

    def parse_text(self):
        #need to parse gkeep 'text' into note components
        #regex for hashtags
        #regex for id datestring

        pass

    

    def write_note(self):
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