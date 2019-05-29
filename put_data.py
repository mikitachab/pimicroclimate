import requests


api_url = 'https://pimicroclimate.herokuapp.com/api/measurements/'
local_url = 'http://localhost:8000/api/measurements/'

responce = requests.get(url=api_url)
data_json = responce.json()

for mes in data_json:
    requests.post(url=local_url, data=mes)
