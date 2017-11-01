#!/usr/bin/python3

import rumphybot
import praw
import random
import codecs
from config_bot import *

#reddit stuff
r = praw.Reddit(user_agent = "Rumphybot 1.7 by herumph",
        client_id = ID,
        client_secret = SECRET,
        username = REDDIT_USERNAME,
        password = REDDIT_PASS)

#r.login(REDDIT_USERNAME, REDDIT_PASS)
sub = "RunningCircleJerk"
#sub = "rumphybot"
subreddit = r.subreddit(sub)


#fetching arrays
already_done = rumphybot.get_array("already_done")
threads = rumphybot.get_array("threads")

def url(link, link_len):
    link = r.submission(id = link)
    #getting rid of last whitespace if it exists.
    link_len = len(list(filter(None, link_len)))
    if(link_len < 8):
        url_tit = "**Title** \n \n"+link.title
        if(link.is_self):
            url_text = "\n \n **Text** \n \n"+link.selftext
        if(not link.is_self):
            url_text = "\n \n **Link from post** \n \n"+link.url
        author_text = "\n \n- "+str(link.author)
        sim_text = "\n \n +/u/user_Simulator "+str(link.author)
        new_comment = url_tit+url_text+author_text+sim_text
        return new_comment
    else:
        text = link.comments[0].body
        author = link.comments[0].author
        sim_text = "\n \n +/u/user_Simulator "+str(author)
        new_comment = "**Link comment text** \n \n"+text+"\n \n"+"- "+str(author)+sim_text
        return new_comment

def self(links):
    message = ""
    for i in links:
        try:
            i = "https://www."+i
            link = r.submission(submission_id = i)
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
    #trimming to keep file size down
    if(len(threads) > 20):
        del threads[0]
        del threads[0]

    #comments first
    for comment in r.subreddit(sub).comments(limit=25):
        if(comment.id not in already_done and str(comment.author).lower() != "rumphybot"):
            already_done.append(comment.id)
            #making sure the already_done file doesn't get too big. 
            del already_done[0]
            rumphybot.write_out("already_done",already_done)

            #saving comment
            comment_list = str(comment.body)

            if(comment_list.lower().count("!help")):
                index = threads.index(comment.link_id[-6:])
                message = codecs.decode(threads[index+1], 'unicode_escape')
                #trimming list
                del threads[index]
                del threads[index]
                rumphybot.write_out("threads",threads)
                comment.reply(message)
                return 

            if(comment_list.lower().count("thanks rumphybot")):
                message = rumphybot.thanks(str(comment.author))
                comment.reply(message)
                return
            
            if(comment_list.lower().count("!save")):
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
    for submission in r.subreddit(sub).new(limit=5):
        if(submission.id not in already_done and str(submission.author).lower() != "rumphybot"):
            already_done.append(submission.id)
            del already_done[0]
            rumphybot.write_out("already_done",already_done)

            #link posts
            if(not submission.is_self):
                link = r.submission(url = submission.url)
                link_len = submission.url.split('/')
                message = url(link, link_len)
                message = message.splitlines()
                message = r'\n'.join(map(str, message))
                threads.append(submission.id)
                threads.append(message)
                rumphybot.write_out('threads',threads)
                return

            #self posts
            if(submission.is_self):
                text = submission.selftext
                links = rumphybot.find_links(text)
                message = self(links)
                message = message.splitlines()
                message = r'\n'.join(map(str, message))
                threads.append(submission.id)
                threads.append(message)
                rumphybot.write_out('threads',threads)
                return

    return

main()
