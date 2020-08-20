import urllib.request
from bs4 import BeautifulSoup
import re
import sys
import os

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import mpld3

import json

class DiffData:
    def __init__(self, url):
        self.away = None
        self.home = None
        self.data = None

        page = self.get_page(url)
        self.get_shots(page)


    def get_page(self, url):
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')
        return soup

    def get_shots(self, page):
        teams = page.find_all('a', itemprop='name')
        away = teams[0].text
        home = teams[1].text

        pbp = page.find('table', {'id': 'pbp'})
        rows = pbp.find_all('tr')
        quarter = -1

        diff_time = np.zeros([0,2], dtype=np.int32)
        diff = 0

        for r in rows:
            score = re.match('\n(.+)\:(.+)\..*\n.*\+(.)(.)', r.text)
            if score:
                time = (((12 - int(score.group(1))) * 60) - (int(score.group(2)))) + (quarter*12*60)
                if score.group(4).isdigit():
                    diff -= int(score.group(3))
                else:
                    diff += int(score.group(3))

                if diff_time.size > 0:
                    diff_time = np.append(diff_time, [diff_time[-1]], axis=0)
                    diff_time[-1][0] = time

                diff_time = np.append(diff_time, [np.array([time, diff])], axis=0)
            else:
                try:
                    r['id']
                    quarter += 1
                except: 
                    pass

        np.savetxt('test.csv', diff_time, delimiter=',')
        self.away = away
        self.home = home
        self.data = diff_time


if __name__ == "__main__":
    # with open('colours.json') as json_file:
    #     colours = json.load(json_file)
    
    diff = DiffData('https://www.basketball-reference.com/boxscores/pbp/202008170TOR.html')
    print(diff.data)