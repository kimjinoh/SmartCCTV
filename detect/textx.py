import requests
resp = requests.post('https://textbelt.com/text', {
  'phone': '+8227390744',
  'message': 'Hello world',
  'key': 'textbelt',
})
print(resp.json())
