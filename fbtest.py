'''
Created on Feb 10, 2016
@author: hanhanwu
Use the code here to test Facebook Graph API
'''

import facebook
import requests
 
 
# Get your temporary token: https://developers.facebook.com/tools/explorer/
access_token = '[your temporary token]'
user = 'me'
 
graph = facebook.GraphAPI(access_token)
profile = graph.get_object(user)
friends = graph.get_connections(profile['id'], 'friends')

 
# Wrap this block in a while loop so we can keep paginating requests until finished.
while True:
        try:
            for friend in friends['data']:
                print friend['name'], friend['id']
            # Attempt to make a request to the next page of data, if it exists.
            friends = requests.get(friends['paging']['next']).json()
        except KeyError:
            # When there are no more pages (['paging']['next']), break from the loop and end the script.
            break


