

__author__ = "Jason M. Pittman"
__copyright__ = "Copyright 2022"
__credits__ = ["Jason M. Pittman"]
__license__ = "GPLv3"
__version__ = "0.1.0"
__maintainer__ = "Jason M. Pittman"
__email__ = "jason@jasonmpittman.com"
__status__ = "Development"


class Note:

    __header = {
        'id': '',
        'title': '',
        'body': '',
        'tags': []
    }

    def __init__(self, n):
        self.__header['title'] = n.title # i think we need to parse the short sentence from n.Text
        self.__header['body'] = n.text
        self.__header['id'] = n.title #the title in gkeep is the date based id
        self.__header['tags'] = n.labels

        #print(self.__header)