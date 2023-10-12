from requests import get
from json import loads

url = 'https://instagram.com/iamjuse'

params = { '__a': 1, '__d': 1 }

cookies = { 'sessionid': '635954753%3AMR2e92kELPo7KN%3A28%3AAYe7El72Yax2XD-K1ailWbaWDkDB3l2JvRkZ6kZlZw' }

def on_success(response):
    profile_data_json = response.text
    parsed_data = loads(profile_data_json)
    print(parsed_data)
    
    # print('User fullname:', parsed_data['graphql']['user']['full_name'])
    # print('User bio:', parsed_data['graphql']['user']['biography'])

def on_error(response):
    print('Something went wrong')
    print('Error Code:', response.status_code)
    print('Reason:', response.reason)


response = get(url, params, cookies=cookies)

if response.status_code == 200:
    on_success(response)
else:
    on_error(response)