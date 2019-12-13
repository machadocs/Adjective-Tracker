import pickle

def getAdjsTimes(dictFox):
    import requests
    from bs4 import BeautifulSoup
    import enchant
    dctnry = enchant.Dict("en_US")
    import nltk
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')

    base_url = 'https://www.cnn.com/politics'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'
    }
    r = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")
    print(soup.prettify())


    '''
    base_url = 'https://www.cnn.com/'
    r = requests.get(base_url)
    soup = BeautifulSoup(r.text, "html.parser")
    print(soup.prettify())
    '''

    #print(r.text)
    #print(titles)
    new = {}

    for story_heading in soup.find_all(class_="cd__headline-text"):
        print(story_heading)
        if story_heading.a and story_heading.a.text != "":
            text = story_heading.a.text.replace("-", " ").strip()
            print(text)
            pairs = nltk.word_tokenize(text)
            for pair in nltk.pos_tag(pairs):
                if not dctnry.check(pair[0]):
                    continue
                elif pair[1] == "JJ":
                    if pair[0] not in new.keys():
                        new[pair[0]] = 1
                    else:
                        new[pair[0]] += 1
    return new


def save(dictFox):
    pickle.dump(dictFox, open("NYTAdjectives.p", "wb"))


def load():
    return pickle.load(open("NYTAdjectives.p", "rb"))


def clear():
    pickle.dump({}, open("NYTAdjectives.p", "wb"))


def sortPrint():
    d = load()
    print(d)
    """
    for w in sorted(d, key=d.get, reverse=True):
        print(w, d[w])
    """


if __name__ == '__main__':
    clear()
    save(getAdjsTimes(load()))
    print("results****************************************************")
    sortPrint()

    '''
    print("Hello! Welcome to the New York Times adjective capturer. "
          "This program can find all of the adjectives on the NYT Home site "
          "and continually store their frequencies! Why you ask? Because. Cheers!")

    choices = ["run", "print", "clear", "quit"]
    choice = ""

    while True:
        while choice not in choices:
            print("\n"+"*"*23+
                  "\n* Available Commands *"
          "\nrun, print, clear, quit"
                  "\n"+'*'*23)
            choice = input("-->")

        if choice == "print":
            print("printing...\n \n"+"-"*23)
            sortPrint()

        elif choice == "run":
            print("running...\n \n"+"-"*23)
            dict = load()
            getAdjsFox(dict)
            save(dict)
            print('Done!')

        elif choice == 'clear':
            while choice != 'yes' and choice != 'no':
                choice = input("Are you sure you want to clear the data? "
                               "It will be lost forever if you do... (yes/no)\n")
            if choice == 'yes':
                print("clearing...\n \n"+"-"*23)
                clear()
                print("Data erased!")
            if choice == 'no':
                print('Good choice!')

        else:
            break

        print("-" * 24 + "\n")
        choice = ''

    print("Thanks for stopping by! Hope you weren't too disturbed ;)")
    '''
