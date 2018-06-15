# import libraries
import re
import tweepy
import os
import time
from secrets import *
from urllib import request
from bs4 import BeautifulSoup
from airtable import airtable

at = airtable.Airtable(os.environ['airtable_indextrump_base'], os.environ['airtable_apikey'])
at.get('IndexTrump')

def send_tweet(paper, trumpindex):
    # Twitter requires all requests to use OAuth for authentication
    auth = tweepy.OAuthHandler(os.environ["consumer_key"], os.environ["consumer_secret"]) 

    auth.set_access_token(os.environ["access_token"], os.environ["access_secret"])

     #Construct the API instance
    api = tweepy.API(auth) # create an API object

    user = api.me()
    print (user.name)

    update = "Today's " + paper[0] + " homepage features " + str(trumpindex) + " mentions of Trump " + paper[1] + " #TrumpIndex"

    send_update(api, update)


def send_update(api, txt):

    # send the status update
    try:

        status = api.update_status(txt)
        print (status.id)
    except Exception as e:
        print(e)

#updates the Airtable record for today with the page & index
def update_airtable(dbrec, paper, index):
    at.update('IndexTrump', dbrec, {paper: index})

def get_index():

    # pages we track

    tracking_papers = [("Washington Post","https://www.washingtonpost.com", "@WashingtonPost"),
                       ("Chicago Tribune","https://www.chicagotribune.com", "@chicagotribune"),
                       ("New York Times","https://www.nytimes.com", "@nytimes"),
                       ("CNN","https://www.cnn.com", "@cnn"),
                       ("Fox News","https://www.foxnews.com", "@FoxNews"),
                       ("NBC News","https://www.nbcnews.com/", "@nbcnews"),
                       ("CBS News","https://www.cbsnews.com/","@CBSNews"),
                       ("ABC News","https://abcnews.go.com/","@ABC"),
                       ("The Guardian","https://www.theguardian.com/us","@GuardianUS")]

    # Create a new record in Airtable
    dbrec = at.create('IndexTrump', {'Date': now.strftime("%Y-%m-%d")})

    for paper in tracking_papers:
        try:
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

            # update the database
            update_airtable(dbrec, paper[0], len(alltrumps))

            # send the tweet!
#            send_tweet(paper, len(alltrumps))
            # and wait a few sec before the next one
            time.sleep(10)
        except Exception as e:
            print(e)
	  


if __name__ == '__main__':
    get_index()
