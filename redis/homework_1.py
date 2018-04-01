#this script should be run with python3. Running it with python instead of python3 gives an Import Error since requests module is not installed with python2 
import requests

base_url = 'https://api.nasa.gov/planetary/apod?api_key=J4MeFBGgCuwzbDu5BfdDIveZjfhhMUH29v7bXTJQ&'
date = 'date=2017-08-09'
request_url = base_url + date

result = requests.get(request_url).json()
print(result['url'])
