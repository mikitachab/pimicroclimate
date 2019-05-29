import requests


api_url = 'https://pimicroclimate.herokuapp.com/api/measurements/'
local_url = 'http://127.0.0.1:8000/'

responce = requests.get(url=api_url)
data_json = responce.json()

for mes in data_json:
    requests.post(url=local_url, data=mes)
