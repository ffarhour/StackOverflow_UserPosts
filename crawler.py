"""This script finds all the posts by a specific user which include the words 'vulnerability', 'vulnerable' or 'vulnerabilities'

Author: Farmehr Farhour f.farhour@gmail.com
"""

from lxml import html
from lxml import etree
import requests
import os.path, sys

global g_xml_namespace
g_xml_namespace = "http://www.w3.org/XML/1998/namespace"

class bcolors:
    """Used to implement ANSI colors without the need to remember the numbers.
    Does not contain any methods. Only contains variables.
    Usage: simply concatenate bcolors.<color> at the start of string to be printed,
        and bcolors.ENDC at the end of the string, to color the string with the
        specified color.
    """

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


#function to save string to file
def saveToFile(string, filename):
    """saves xml to file"""
    #increment name no. if already exists
    n = 0
    while(os.path.isfile(filename + str(n) + ".txt")==True):
        n = n+1
    f = open(filename+str(n)+".txt", 'w')
    f.write(string)
    f.close()
    print(bcolors.OKGREEN + "All done! Filename: "+ filename + str(n) + ".txt" + bcolors.ENDC)

def getHTMLstring(url):
    """returns html string from url (utf-8 encoding)"""
    page = requests.get(url)
    return page.content.decode("utf-8")

def getHtml(url):
    """returns html tree from url"""
    page = requests.get(url)
    tree = html.fromstring(page.content)
    tree.make_links_absolute(url,resolve_base_href=True)
    return tree

def check_containsWord(word,string):
    """returns true if word exists in string. Otherwise returns false"""
    return word in string

def main(argv):
    print(bcolors.HEADER + __doc__ + bcolors.ENDC)
    username_url = input(bcolors.WARNING + "Please enter the url of the user profile: " + bcolors.ENDC) or "http://stackoverflow.com/users/10080/avid"
    username = str(username_url.rsplit('/', 1)[-1])
    #parse the url and get html tree

    #count used to print out the progress
    progress_count = 0

    #get all user answers
    user_answers = []
    max_page = 2;
    page = 1;
    while(page<max_page+1):
        username_url_tree = getHtml(username_url + "?tab=answers&sort=newest&page="+str(page))
        if(1==page):
            max_page = len(username_url_tree.xpath(".//div[@class='user-tab-footer']//div[@class='pager fr']//a"))
        user_answers = user_answers + username_url_tree.xpath(".//div[@class='user-answers']//div[@class='answer-link']//a/@href")
        page = page + 1

    #print(user_answers)
    print(bcolors.OKGREEN + "Number of answers posted by " + str(username_url.rsplit('/', 1)[-1]) + " = " + str(len(user_answers)) + bcolors.ENDC)

    #filter answers if they contain "vulnerab"
    answers_with_word = []
    print(bcolors.UNDERLINE + "Progress" + bcolors.ENDC)
    for link in user_answers:
        sys.stdout.write("\r{0:.2f}".format((float(progress_count)/len(user_answers))*100) + "%")
        sys.stdout.flush()
        word = "vulnerab"
        #print(link)
        html = getHTMLstring(link)
        if(check_containsWord(word,html)):
            answers_with_word.append(link)
        progress_count = progress_count + 1;

    sys.stdout.write("\r{0:.2f}".format((float(1))*100) + "%")
    sys.stdout.flush()

    print(bcolors.OKGREEN + "\nNumber of answers posted by " + username + " that contain 'vulnerability', 'vulnerable' or 'vulnerabilities' = " + str(len(answers_with_word)) + bcolors.ENDC)

    #print(answers_with_word)
    links_string = ""
    for link in answers_with_word:
        links_string = links_string + link + "\n"
    saveToFile(links_string,username+"_answers")



if __name__ == "__main__":
    main(sys.argv)
