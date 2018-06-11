# import libraries
import re
import tweepy
from secrets import *
from urllib import request
from bs4 import BeautifulSoup


def send_tweet(paper, trumpindex):
    # Twitter requires all requests to use OAuth for authentication
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 

    auth.set_access_token(access_token, access_secret)

     #Construct the API instance
    api = tweepy.API(auth) # create an API object

    user = api.me()
    print (user.name)

    # send the status update
    try:
        update = "Today's #TrumpIndex for " + paper + " = " + str(trumpindex)

        status = api.update_status(update)
        print (status.id)
    except Exception as e:
        print(e)

def get_index():

    # pages we track

    tracking_papers = [("Washington Post","https://www.washingtonpost.com"),
                       ("Chicago Tribune","https://www.chicagotribune.com"),
                       ("New York Times","https://www.nytimes.com"),
                       ("CNN","https://www.cnn.com"),
                       ("NBC News","https://www.nbcnews.com/")]

    for paper in tracking_papers:
        print(paper[0])
        page = request.urlopen(paper[1])
        soup = BeautifulSoup(page, 'html.parser')
        # test
        print(soup.title)
        # find all the Trumps
        # get the text first
        alltext = soup.get_text()

        alltrumps = [m.start() for m in re.finditer('Trump', alltext)]
    
        #alltrumps = soup.find_all(string="Trump")
        print(len(alltrumps))

        # send the tweet!
#        send_tweet(paper[0], len(alltrumps))
	  
        #and show 'em
#        for tr in alltrumps:
            # show 10 chars either side
#            print(alltext[tr-15:tr+20])



if __name__ == '__main__':
    get_index()
