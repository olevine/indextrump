# import libraries
import re
import tweepy
import os
import time
from airtable import Airtable
from secrets import *
from urllib import request
from bs4 import BeautifulSoup
import datetime

at = Airtable(os.environ['airtable_indextrump_base'], 'TrumpIndex', api_key=os.environ['airtable_apikey'])

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
    at.update(dbrec['id'], {paper: index})

def test_new():

#	tracking_papers = [("Washington Post","https://www.washingtonpost.com", "@WashingtonPost"),
#                       ("Chicago Tribune","https://www.chicagotribune.com", "@chicagotribune"),
#                       ("New York Times","https://www.nytimes.com", "@nytimes"),
#                       ("CNN","https://us.cnn.com", "@cnn"),
#                       ("Fox News","https://www.foxnews.com", "@FoxNews"),
#                       ("MSNBC","https://www.msnbc.com", "@msnbc"),
#                       ("NBC News","https://www.nbcnews.com/", "@nbcnews"),
#                       ("CBS News","https://www.cbsnews.com/","@CBSNews"),
#                       ("ABC News","https://abcnews.go.com/","@ABC"),
#                       ("The Guardian","https://www.theguardian.com/us","@GuardianUS")]
	
	tracking_papers = [("NPR","https://www.npr.org/sections/news/", "@npr")]

	for paper in tracking_papers:
		try:
			print(paper[0])
			page = request.urlopen(paper[1])
			soup = BeautifulSoup(page, "html.parser")
			print(soup.title)
			
			# initiate the list of found strings
			matches = []
			
			# find all article headers
#			headers = soup.find_all([re.compile("^h[1-5]"),"span","p","a","strong"])
			headers = soup.find_all(string=re.compile("Trump"))
			hcount = 0
			trcount = 0
    
			for hdr in headers:
				hcount += 1
				#for hstr in hdr.contents:
					#if (hstr.find('Trump') > 1):
						#trcount += 1
				try:
					mi = matches.index(hdr)
				# new value: add to array
				except ValueError:
					matches.append(hdr)
					trcount += 1
					#print(hdr.name, hstr)
				
				#if (hdr.contents and hdr.contents.string.find('Trump') > -1):
				#	trcount += 1
				#	print(hdr.name, hdr.contents)
			print(hcount, trcount)
			
			# get the text first
			alltext=soup.get_text()
			
			alltrumps = [m.start() for m in re.finditer('Trump ', alltext)]
			
			print(len(alltrumps))

		except Exception as e:
			print(e)


def get_index():

    # pages we track

    tracking_papers = [("Washington Post","https://www.washingtonpost.com", "@WashingtonPost"),
                       ("Chicago Tribune","https://www.chicagotribune.com", "@chicagotribune"),
                       ("Los Angeles Times","http://www.latimes.com/", "@latimes"),
                       ("New York Times","https://www.nytimes.com", "@nytimes"),
                       ("NPR","https://www.npr.org/sections/news/", "@npr"),
                       ("Fox News","https://www.foxnews.com", "@FoxNews"),
                       ("MSNBC","https://www.msnbc.com", "@msnbc"),
                       ("NBC News","https://www.nbcnews.com/", "@nbcnews"),
                       ("CBS News","https://www.cbsnews.com/","@CBSNews"),
                       ("ABC News","https://abcnews.go.com/","@ABC"),
                       ("The Guardian","https://www.theguardian.com/us","@GuardianUS")]

    # Create a new record in Airtable
    dbrec = at.insert({'Date': datetime.datetime.now().strftime("%Y-%m-%d")})

    for paper in tracking_papers:
        try:
            print(paper[0])
            page = request.urlopen(paper[1])
            soup = BeautifulSoup(page, 'html.parser')
            # test
            #print(soup.title)

            matches = []

            # look only at headers, <span>, <p>
            headers = soup.find_all(string=re.compile("Trump"))
            hcount=0
            trcount=0
			
            for hdr in headers:
                hcount += 1
				
                #look for duplicates
                try:
                    mi = matches.index(hdr)
                except ValueError:
                    # new value
                    matches.append(hdr)
                    trcount += 1
			
            #get the text first
            #alltext=soup.get_text()
            #alltrumps = [m.start() for m in re.finditer('Trump ', alltext)]

            #print(len(alltrumps))

            # update the database
            update_airtable(dbrec, paper[0], trcount)

            # send the tweet!
            send_tweet(paper, trcount)
            # and wait a few sec before the next one
            time.sleep(5)
        except Exception as e:
            print(e)
	  

if __name__ == '__main__':
    get_index()
    #test_new()
