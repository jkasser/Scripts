from fbchat import Client
from fbchat.models import *
from random import choice
from time import sleep
from datetime import datetime, timedelta
from dateutil import parser
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(__file__, "..")))
from .config import  *


class PostImage:
    EVENT_FILE = './events.txt'
    PIC_DIR = './data'

    def __init__(self):
        self.client = self.fb_login()

    def fb_login(self):
        self.client = Client(FB_UN, FB_PW)
        return self.client

    def check_login_status(self):
        if not self.client.isLoggedIn():
            self.fb_login()

    def post_to_facebook(self):
        if len(os.listdir(self.PIC_DIR)) > 0:
            if len(os.listdir(self.PIC_DIR)) == 1:
                self.client.sendMessage(message=Message('This is my last photo!!! Better restock me...'),
                                        thread_id=GROUP_CHAT_ID, thread_type=ThreadType.GROUP)
            random_pic = choice(os.listdir(self.PIC_DIR))
            file = os.path.abspath(f'{self.PIC_DIR}/{random_pic}')
            self.client.sendLocalImage(file, message=Message(text=', '.join((str(random_pic).split('.')[0]).split('_'))), thread_id=GROUP_CHAT_ID, thread_type=ThreadType.GROUP)
            os.remove(file)
        else:
            self.client.sendMessage(message=Message('Hey you putz! I\'m out of pictures to send!'), thread_id=GROUP_CHAT_ID, thread_type=ThreadType.GROUP)

    def check_if_should_post(self):
        with open(self.EVENT_FILE, 'r') as f:
            for line in f.readlines():
                if 'last_post' in line:
                    last_write_time = line.split(':')[1]
                    next_post_time = self.calc_time_elapsed(last_write_time)
                    if datetime.utcnow() >= next_post_time:
                        return True
                    else:
                        return False

    def calc_time_elapsed(self, last_write_time):
        next_post_time = parser.parse(last_write_time) + timedelta(hours=23, minutes=59)
        return next_post_time

    def write_last_post_time(self, new_time):
        with open(self.EVENT_FILE, 'w') as f:
            f.write(f'last_post:{new_time}')

if __name__ == '__main__':
    pi = PostImage()
    while True:
        if pi.check_if_should_post():
            # login if we arent anymore
            pi.check_login_status()
            # post something here
            print('Time to post! Attempting post now...')
            pi.post_to_facebook()
            # write the current time
            pi.write_last_post_time(datetime.utcnow())
        else:
            print(f'Not time yet! Current time is {datetime.utcnow()}, sleeping for 5 minutes')
            sleep(600)
