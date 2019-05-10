from fbchat import Client
from fbchat.models import *
import os
from random import choice
from datetime import datetime, timedelta
from dateutil import parser
from wtpics.config import FB_PW, FB_UN, GROUP_CHAT_ID


class PostImage:
    EVENT_FILE = './events.txt'
    PIC_DIR = './data'

    def fb_login(self):
        self.client = Client(FB_UN, FB_PW)
        return self.client

    def post_to_facebook(self):
        random_pic = choice(os.listdir(self.PIC_DIR))
        file = os.path.abspath(f'{self.PIC_DIR}/{random_pic}')
        self.client.sendLocalImage(file, message=Message(text=', '.join((str(random_pic).split('.')[0]).split('_'))), thread_id=GROUP_CHAT_ID, thread_type=ThreadType.GROUP)
        os.remove(file)

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
    if pi.check_if_should_post():
        # login
        pi.fb_login()
        # post something here
        pi.post_to_facebook()
        # write the current time
        pi.write_last_post_time(datetime.now())