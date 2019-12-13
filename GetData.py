import pickle
import requests
from bs4 import BeautifulSoup
import enchant
import csv
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def getSoup(p, url):
    r = requests.get(url)
    if p: #print
        return r.text
    else: #no print
        return BeautifulSoup(r.text, features="html.parser")

def getAdjs(d, clss, url):
    dctnry = enchant.Dict("en_US")
    soup = getSoup(False, url)

    new = {}

    for story_heading in soup.find_all(class_=clss):
        if story_heading.a and story_heading.a.text != "":
            text = story_heading.a.text.replace("-", " ").strip()
            pairs = nltk.word_tokenize(story_heading.a.text)
            for pair in nltk.pos_tag(pairs):
                if not dctnry.check(pair[0]):
                    continue
                elif pair[1] == "JJ":
                    if pair[0] not in new.keys():
                        new[pair[0]] = 1
                    else:
                        new[pair[0]] += 1
    if not new:
        return "Error: Check soup.find_all() to make sure you are searching for the correct class."
    #master.update({key: new})
    d.update(new)
    return new


def save(d):
    pickle.dump(d, open("Data.p", "wb"))

def load():
    return pickle.load(open("Data.p", "rb"))

def clear():
    pickle.dump({}, open("Data.p", "wb"))

def sortPrint(d):
    try:
        for w in sorted(d, key=d.get, reverse=True):
            print(w, d[w])
    except:
        print("Data is messed up. Check SiteInfos.txt to make sure you are looking for the correct class tag.")

def getSiteInfos():
    with open('SiteInfos.txt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        infos = {}
        for row in csv_reader:
            infos[row[0]] = {'url': row[1], 'class': row[2]}
            line_count += 1
    return infos

def sure(action):
    choices = ['y', 'n']
    choice = ''
    while choice not in choices:
        choice = input("Are you sure you want to continue with " + action +
                       "? You may lose data forever. (y/n)\n")
    if choice == 'n':
        print("OK! I will not " + action)
    return choice == 'y'

def getActions(choices):
    choice = ''
    while choice not in choices:
        print("\n" + "*" * 23 +
              "\n* Available Commands *"
              "\n" + str(choices) +
              "\n" + '*' * 23)
        choice = input("-->")
    return choice

if __name__ == '__main__':
    print("Hello! Welcome to the News adjective capturer. "
          "This program can find all of the adjectives on Various News sites "
          "and continually store their frequencies! Why you ask? Because. Cheers!")


    master = load()
    infos = getSiteInfos()
    d = {}
    level = 0
    site = ''
    while True:
        if level == 0:
            choices = ["checkout", "print", "clear", "quit", "save"]
            choice = ""
            while choice not in choices:
                print("\n" + "*" * 23 +
                      "\n* Available commands *"
                      "\n" + str(choices) +
                      "\n" + '*' * 23)
                choice = input("-->")
            if choice == 'checkout':
                while choice not in infos.keys():
                    print("\n" + "*" * 23 +
                          "\n* Choose the site to use, available sites: *"
                          "\n" + str(infos.keys()) +
                          "\n" + '*' * 23)
                    choice = input("-->")
                if choice in master.keys():
                    d = master[choice]
                level = 1
                site = choice
            elif choice == 'print':
                print(master)
            elif choice == 'clear':
                if sure(choice):
                    print("clearing...\n \n" + "-" * 23)
                    master = {}
                    clear()
                    print("Data erased!")
            elif choice == 'save':
                if sure(choice):
                    save(master)
            else:
                break
        if level == 1:
            choices = ["run", "print", "clear", "quit", "results", "merge", 'back']
            choice = getActions(choices)
            if choice == "results":
                print("printing...\n \n" + "-" * 23)
                sortPrint(d)
            elif choice == "run":
                print("running...\n \n" + "-" * 23)
                d = getAdjs(d, infos[site]['class'], infos[site]['url'])
                print('Done!')
            elif choice == 'merge':
                if sure(choice):
                    master.update({site: d})
            elif choice == 'clear':
                print('Which site specific dict would you like to clear?')
                choices = ['current', 'master']
                choice = getActions(choices)
                if sure("clear from " + choice):
                    if choice == 'current':
                        print("clearing...\n \n" + "-" * 23)
                        d = {}
                        print("Current " + site + " data erased!")
                    else:
                        print("clearing...\n \n" + "-" * 23)
                        master.update({site: {}})
                        save(master)
                        print(site.capitalize() + " dict erased in master!")
            elif choice == 'print':
                print(getSoup(True, infos[site]['url']))
            elif choice == 'back':
                level = 0
            else:
                break

            print("-" * 24 + "\n")
            choice = ''

    print("Thanks for stopping by! Hope you weren't too disturbed ;)")



