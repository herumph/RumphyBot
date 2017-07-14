#!/Users/sfdavis/anaconda3/bin/python

#Bot to save linked threads before they are deleted or removed by a mod. Last updated 12/03/16.

import praw
import os.path
import re
from config_bot import *
from datetime import *
import random

#Reddit stuff
r = praw.Reddit("ARprojectbot 1.0 by herumph")
r.login(REDDIT_USERNAME, REDDIT_PASS)
subreddit = r.get_subreddit("RumphyBot")
#subreddit = r.get_subreddit("AdvancedRunning")
subreddit_comments = subreddit.get_comments()

#Functions to read and write files into arrays.
def get_array(input_string):
	with open(input_string+".txt","r") as f:
		input_array = f.readlines()
	input_array = [x.strip("\n") for x in input_array]
	return(input_array)

def write_out(input_string,input_array):
	with open(input_string+".txt","w") as f:
		for i in input_array:
			f.write(i+"\n")
	return

#Fetching arrays
already_done = get_array("already_done")
post = get_array("post")
saved_posts = get_array("saved_posts")

print("\n * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * \n")
copypasta="I'm JustARunner and this is my ADVANCED RUNNING PROJECT. I work here with my old man and my son, cockswick. Everything in here has a story and a price for me to sellout. One thing I've learned after 20 years - you never 101% know what is gonna come through that door."

#Looking through 2 newest submissions. RCJ isn't super busy so no need to look past that.
for submission in subreddit.get_new(limit=2):
    if(str(submission.author) == 'AutoModerator' and submission.id not in already_done):
        already_done.append(submission.id)
        write_out("already_done",already_done)
        submission.add_comment(copypasta)
        submission.add_comment('Hello bot brother! BEEP BOOP')
