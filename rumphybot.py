#!/usr/bin/python3

#Rumphybot 1.5
#Bot to save linked threads before they are deleted or removed by a mod.

#functions to read and write files into arrays.
def get_array(input_string):
	with open("textfiles/"+input_string+".txt","r") as f:
		input_array = f.readlines()
	input_array = [x.strip("\n") for x in input_array]
	return(input_array)

def write_out(input_string,input_array):
	with open("textfiles/"+input_string+".txt","w") as f:
		for i in input_array:
			f.write(i+"\n")
	return

#looking at urls
def url(link, link_len):
        #getting rid of last whitespace if it exists.
        link_len = len(list(filter(None, link_len)))
        if(link_len < 8):
            url_tit = "**Title** \n \n"+link.title
            url_text = "\n \n **Text** \n \n"+link.selftext
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

#responding to thanks messages
def thanks(author):
    personal_messages = get_array("personal_messages")
    if(personal_messages.count(author)):
        index = personal_messages.index(author)
        return personal_messages[index+1]
    else:
        message = "No problem <3"
        return message

#replying to save requests. Basically the same as going through self posts.
def find_links(comment_list):
    reddit_index = [n for n in range(len(comment_list)) if comment_list.find("reddit.com",n) == n]
    links = []
    for i in reddit_index:
        temp = comment_list[i:]
        temp = temp.split()
        #getting rid of fancy format parenthesis.
        temp = temp[0].split(')',1)
        links.append(temp[0])
    return links
