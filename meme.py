import requests
import urllib
from decouple import config

username = config("LOGIN")
password = config("PASSWORD")

userAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"

#Fetch the available memes
data = requests.get('https://api.imgflip.com/get_memes').json()['data']['memes']
images = [{'name':image['name'],'url':image['url'],'id':image['id']} for image in data]

def make_meme(upper, lower):
    id = 23
    text0 = upper
    text1 = lower

    #Fetch the generated meme
    URL = 'https://api.imgflip.com/caption_image'
    params = {
        'username':username,
        'password':password,
        'template_id':images[id-1]['id'],
        'text0':text0,
        'text1':text1
    }
    response = requests.request('POST',URL,params=params).json()
    print(response)

    #Save the meme
    opener = urllib.request.URLopener()
    opener.addheader('User-Agent', userAgent)
    return response['data']['url']