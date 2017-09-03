#!/usr/bin/python3

import rumphybot
import praw
import random
from config_bot import *

#reddit stuff
r = praw.Reddit("Rumphybot 1.5 by herumph")
r.login(REDDIT_USERNAME, REDDIT_PASS)
subreddit = r.get_subreddit("RumphyBot")
#subreddit = r.get_subreddit("RunningCirclejerk")
subreddit_comments = subreddit.get_comments()


#fetching arrays
already_done = rumphybot.get_array("already_done")

print("* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * ")

def self(links):
    message = ""
    for i in links:
        try:
            i = "https://www."+i
            link = r.get_submission(submission_id = i)
            link_len = i.split('/')
            message += rumphybot.url(link, link_len)
        except:
            pass
        if(len(links) > 1 and i != "https://www."+links[-1]):
            message += "\n\n*****\n\n"
    if(not message.count("Title")):
        message = "No valid links."
    return message


def main():
    #comments first
    for comment in subreddit_comments:
        if(comment.id not in already_done and str(comment.author).lower() != "rumphybot"):
            already_done.append(comment.id)
            #making sure the already_done file doesn't get too big. 
            del already_done[0]
            rumphybot.write_out("already_done",already_done)

            #saving comment
            comment_list = str(comment.body)

            if(comment_list.lower().count("thanks rumphybot")):
                message = rumphybot.thanks(str(comment.author))
                comment.reply(message)
                return
            
            if(comment_list.lower().count("rumphybot save")):
                message = ""
                links = rumphybot.find_links(comment_list)
                message = self(links)
                comment.reply(message)
                return

            if(comment_list.lower().count("rumphybot what do")):
                what_do = rumphybot.get_array("what_do")
                message = random.choice(what_do)
                comment.reply(message)
                return

            if(comment_list.lower().count("shin splints")):
                message = "You're such a special little snowflake with your [weak shins.](https://youtu.be/hexYeGlgD0c?t=86)"
                comment.reply(message)
                return

            if(comment_list.lower().count("fuck off rumphybot")):
                message = "http://imgur.com/08gDI9E"
                comment.reply(message)
                return

    #new threads
    for submission in subreddit.get_new(limit=2):
        if(submission.id not in already_done and str(comment.author).lower() != "rumphybot"):
            already_done.append(submission.id)
            del already_done[0]
            rumphybot.write_out("already_done",already_done)

            #link posts
            if(not submission.is_self):
                link = r.get_submission(submission_id = submission.url)
                link_len = submission.url.split('/')
                message = rumphybot.url(link, link_len)
                submission.add_comment(message)
                return

            #self posts
            if(submission.is_self):
                text = submission.selftext
                links = rumphybot.find_links(text)
                message = self(links)
                submission.add_comment(message)
                return

    return

main()
