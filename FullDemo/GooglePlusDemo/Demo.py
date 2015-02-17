import GooglePlusSearch

'''As is, this code uses the google_api.txt key in this folder. 
Currently, I have inserted a key registed to myself, Luke Lindsey.'''

#example query
query = "hello"

GooglePlusSearch.mySearch(query)

#The below documentation is also in the search code, but I felt it would be useful here too.

'''To find the post value, instead of printing item on the search method we could have
object = item["object"]
content = object["content"]

date is listed at:
updated = item["updated"]'''

