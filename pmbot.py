#!/Users/sfdavis/anaconda3/bin/python

#bot to PM users that responded to the JAR letter

import praw
import os.path
import re
from config_bot import *
from datetime import *
import random

#Reddit stuff
r = praw.Reddit("PMbot 1.0 by herumph")
r.login(REDDIT_USERNAME, REDDIT_PASS)

print("\n * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * \n")

letter=r.get_submission('https://www.reddit.com/r/RumphyBot/comments/6n9aws/testing_copypasta/dk7ol0a/')
#letter=r.get_submission('https://www.reddit.com/r/AdvancedRunning/comments/6mm2a7/an_open_letter_from_the_community_to_ujustarunner/dk2j2mo/')
letter.replace_more_comments(limit=None, threshold=0)
comments=praw.helpers.flatten_tree(letter.comments)
print(len(comments))
supporters=[]
for comment in comments:
    supporters.append((comment.author))

supporters=supporters[3:]
#print(supporters)
subject="Hi!  We’d like to invite you to /r/ARTC"
msg=""
for user in supporters:
    r.send_message(user, subject, msg)
