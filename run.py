#!/usr/bin/python
import os

user_name = None #add the computer user name here instead of None.
os.system('crontab -e [-u {}] */10  * * * * /usr/bin/python reminder.py'.format(user_name))