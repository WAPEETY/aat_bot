from json import load as jsonLoad
from os.path import abspath, dirname, join


with open(join(dirname(abspath(__file__)), "replies_list.json")) as replies_file:
    json_replies = jsonLoad(replies_file)

def getLenght():
    return len(json_replies)

def getName(i):
    if(i < getLenght()):
        return json_replies[i]["name"]
    return "ERROR, Index out of range"

def getDescription(i):
    if(i < getLenght()):
        return json_replies[i]["description"]
    return "Index out of range"

def getContent(i):
    if(i < getLenght()):
        return json_replies[i]["content"]
    return "Hi, this is an error message, go to https://github.com/WAPEETY and blame me in an <b>Issue</b>"
