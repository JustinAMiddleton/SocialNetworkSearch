#need to install requests to run this on your machine
#would be beneficial to make this portable
import requests
import sys

#variable for the api key
GOOGLE_API_KEY = ""

#base url for activity requests to google 
BASE_URL_GOOGLE_PLUS = "https://www.googleapis.com/plus/v1/activities"

#variable for tracking the number of requests to google server
API_REQUEST_COUNT = 0


def setApiKey():
    '''Loads the API key from google_api.txt'''
    global GOOGLE_API_KEY
    try:
        #reads the api key from the google_api.txt file
        fp = open("google_api.txt")
        GOOGLE_API_KEY = fp.readline()
        if GOOGLE_API_KEY == "":
            print("Please place your API key in the google_api.txt file")
            print("If you do not have an API Key from GOOGLE, please register for one at: http://developers.google.com")
            sys.exit(0)
                
        fp.close()
    except IOError:
        print('API Key not found! Please create and fill up google_api.txt file in the same directory which contains the googleplus module')
        print('If you do not have an API Key from GOOGLE, please register for one at: http://developers.google.com')
        sys.exit(0)
    except Exception as e:
        print(e)
        
def defaultSearch(baseUrl,params):

    global API_REQUEST_COUNT 
    try:
        #GET request sent to google
        r = requests.get(baseUrl,params=params)
        API_REQUEST_COUNT +=1
        
        #response in json format converted into a dictionary
        response = eval(r.text)
        return response

    except Exception as e:
        print("Error for URL: ", r.url)
        print(e)
        return { 'status':'ERROR', 'statusInfo':r.status_code }

def mySearch(q,options={}):
  
	#set the API key before placed in payload
    setApiKey() 
    
    #dictionary for containing the GET query parameters.
    payload = {}
    #setting the query parameter
    payload["query"] = q
    #setting the google plus api key
    payload["key"] = GOOGLE_API_KEY
    #setting the parameter for the number of returned results to 20
    payload["maxResults"] = 20
    #setting the order of the returned results to recent.
    payload["orderBy"] = "recent"
    #setting the language parameter to English, so that the returned activity feeds are only in english
    payload["language"] = "en" 
    
    #setting the options if provided, the provided option overrides the default options set above.
    for option in options:
        payload[option] = options[option]

    
    #list for containing the activity items
    allItems = list([])
    
    #response for the first page
    resp = defaultSearch(BASE_URL_GOOGLE_PLUS,payload)
    
    #nextPageToken for looking for further activities
    nextPageToken = resp["nextPageToken"]
    allItems += resp["items"]
    
    while nextPageToken != "":
        #nextPageToken for looking for further activities
        
        #including nestPageToken in the parameters passed for the GET request
        payload["pageToken"] = nextPageToken
        resp = defaultSearch(BASE_URL_GOOGLE_PLUS,payload)
        try:
            nextPageToken = resp["nextPageToken"]
        except KeyError as e:
            #this means no more next page
            break
        allItems += resp["items"]
        
        #could deal with it alternatively here instead. Honestly, that would probably be very smart.
        #Might just want to get the content and date as shown below in the doc string.
        
    for item in allItems:
        #need to do something more meaningful
        #may need to yield to a generator for performance 
        print item
        
        '''To find the post value, instead of printing item on the search method we could have
        
        object = item["object"]
        content = object["content"]

        date is listed at:
        updated = item["updated"]'''
        
    print "There were " + str(API_REQUEST_COUNT) + " requests in this run."
                    


