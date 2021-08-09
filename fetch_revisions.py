import requests
import json

BASE_URL = "http://en.wikipedia.org/w/api.php"
TITLE = 'Donald Trump'

parameters = { 'action': 'query',
           'format': 'json',
           'continue': '',
           'titles': TITLE,
           'prop': 'revisions',
           'rvprop': 'ids|flags|timestamp|userid|user|size|comment|tags',
           'rvlimit': 'max'}

wp_call = requests.get(BASE_URL, params=parameters)
response = wp_call.json()

print(response)



# while True:
#   wp_call = requests.get(BASE_URL, params=parameters)
#   response = wp_call.json()

#   for page_id in response['query']['pages']:
#     total_revisions += len(response['query']['pages'][page_id]['revisions'])

#   if 'continue' in response:
#     parameters['continue'] = response['continue']['continue']
#     parameters['rvcontinue'] = response['continue']['rvcontinue']

#   else:
#     break

# print (parameters['titles'], total_revisions)

with open('donaldtrump_revisions.json', 'w') as f:
    json.dump(response, f)