#!/Users/sfdavis/anaconda3/bin/python

#Bot to save linked threads before they are deleted or removed by a mod. Last updated 12/01/16.

import praw
import os.path
import re
from config_bot import *
import random

#Reddit stuff
r = praw.Reddit("Rumphybot 1.4 by herumph")
r.login(REDDIT_USERNAME, REDDIT_PASS)
subreddit = r.get_subreddit("RumphyBot")
#subreddit = r.get_subreddit("RunningCirlejerk")
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
personal_messages = get_array("personal_messages")
already_done = get_array("already_done")

print("\n * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * \n")

#Looking through 2 newest submissions. RCJ isn't super busy so no need to look past that.
for submission in subreddit.get_new(limit=2):
	#Link posts.
	if(not submission.is_self and submission.id not in already_done):
		#Getting if url is a submission or comment and acting accordingly.
		link = r.get_submission(submission_id = submission.url)
		link_len = submission.url.split('/')
		#Getting rid of last whitespace if it exists.
		link_len = len(list(filter(None, link_len)))
		if(link_len < 8):
			url_tit = "**Title** \n \n"+link.title
			url_text = "\n \n **Text** \n \n"+link.selftext
			author_text = "\n \n- "+str(link.author)
			sim_text = "\n \n +/u/user_Simulator "+str(link.author)
			already_done.append(submission.id)
			write_out("already_done",already_done)
			submission.add_comment(url_tit+url_text+author_text+sim_text)
		else:
			text = link.comments[0].body
			author = link.comments[0].author
			sim_text = "\n \n +/u/user_Simulator "+str(author)
			already_done.append(submission.id)
			write_out("already_done",already_done)
			submission.add_comment("**Link comment text** \n \n"+text+"\n \n"+"- "+str(author)+sim_text)
	#Self posts.
	elif(submission.is_self and submission.id not in already_done):
		text = submission.selftext
		reddit_index = [n for n in range(len(text)) if text.find("reddit.com",n) == n]
		links = []
		for i in reddit_index:
			temp = text[i:]
			temp = temp.split()
			#Getting rid of fancy format parenthesis.
			temp = temp[0].split(')',1)
			links.append(temp[0])
		already_done.append(submission.id)
		write_out("already_done",already_done)
		#Only taking valid links.
		for i in links:
			try:
				link = r.get_submission(submission_id = "https://www."+i)
				link_len = i.split('/')
				#Getting rid of last whitespace caused by ending in a slash.
				link_len = len(list(filter(None, link_len)))
				#Getting if url is a submission or comment and acting accordingly.
				if(link_len < 7):
					url_tit = "**Title** \n \n"+link.title
					url_text = "\n \n **Text** \n \n"+link.selftext
					author_text = "\n \n- "+str(link.author)
					sim_text = "\n \n +/u/user_Simulator "+str(link.author)
					submission.add_comment(url_tit+url_text+author_text+sim_text)
				else:
					text = link.comments[0].body
					author = link.comments[0].author
					sim_text = "\n \n +/u/user_Simulator "+str(author)
					submission.add_comment("**Linked comment text** \n \n"+text+"\n \n"+"- "+str(author)+sim_text)
			except:
				pass

#Sorting through comments and replying
for comment in subreddit_comments:
	#Replying to thanks messages.
	if(comment.body.lower().count("thanks rumphybot") and comment.id not in already_done):
		if(personal_messages.count(str(comment.author))):
			#There's probably a better way to do this but it works well enough.
			for i in range(0,len(personal_messages)-1):
				if(personal_messages[i] == str(comment.author)):
					comment.reply(personal_messages[i+1])
			already_done.append(comment.id)
			write_out("already_done",already_done)
		else:
			comment.reply("No problem <3")
			already_done.append(comment.id)
			write_out("already_done",already_done)

	#Replying to save requests. Basically the same as going through self posts.
	if(comment.body.lower().count("rumphybot save") and comment.id not in already_done):
		text = comment.body
		reddit_index = [n for n in range(len(text)) if text.find("reddit.com",n) == n]
		links = []
		for i in reddit_index:
			temp = text[i:]
			temp = temp.split()
			#Getting rid of fancy format parenthesis.
			temp = temp[0].split(')',1)
			links.append(temp[0])
		already_done.append(comment.id)
		write_out("already_done",already_done)
		#Only taking valid links.
		for i in links:
			try:
				link = r.get_submission(submission_id = "https://www."+i)
				link_len = i.split('/')
				#Getting rid of last whitespace caused by ending in a slash.
				link_len = len(list(filter(None, link_len)))
				#Getting if url is a submission or comment and acting accordingly.
				if(link_len < 7):
					url_tit = "**Title** \n \n"+link.title
					url_text = "\n \n **Text** \n \n"+link.selftext
					author_text = "\n \n- "+str(link.author)
					sim_text = "\n \n +/u/user_Simulator "+str(link.author)
					comment.reply(url_tit+url_text+author_text+sim_text)
				else:
					text = link.comments[0].body
					author = link.comments[0].author
					sim_text = "\n \n +/u/user_Simulator "+str(author)
					comment.reply("**Linked comment text** \n \n"+text+"\n \n"+"- "+str(author)+sim_text)
			except:
				pass

	#Responding to what do with bad advice.
	if(comment.body.lower().count("rumphybot what do") and comment.id not in already_done):
		what_do = get_array("what_do")
		message = random.choice(what_do)
		already_done.append(comment.id)
		write_out("already_done",already_done)
		comment.reply(message)

	#Responding to shin splints.
	if(comment.body.lower().count("shin splints") and comment.id not in already_done):
		already_done.append(comment.id)
		write_out("already_done",already_done)
		comment.reply("You're such a special little snowflake with your [weak shins.](https://youtu.be/hexYeGlgD0c?t=86)")

	#Stalking Shoes.
	if(str(comment.author) == "YourShoesUntied" and comment.id not in already_done):
		hitler_speech = get_array("hitler_speech")
		print(len(hitler_speech))
		message = random.choice(hitler_speech)
		already_done.append(comment.id)
		write_out("already_done",already_done)
		comment.reply(message)

	#Responding to not nice messages.
	if(comment.body.lower().count("fuck you rumphybot") and comment.id not in already_done):
		already_done.append(comment.id)
		write_out("already_done",already_done)
		comment.reply("http://imgur.com/08gDI9E")
