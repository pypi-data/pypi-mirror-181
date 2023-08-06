import requests

class USERS():

    def __init__(self, api_key, user_id=None, group_id=None, fake_count=1):
        self.user_id = user_id
        self.group_id = group_id
        self.fake_count = fake_count
        assert isinstance(api_key, str), 'You must provide a valid API Key'
        self.api_key = api_key

    @property
    def userlist(self):
        path = 'https://app.drchrono.com/api/users'
        list_response = []
        while path:
            data = requests.get(path, headers={'Authorization': 'Bearer ' + self.api_key})
            data_json = data.json()
            list_response.extend(data_json['results'])
            path = data_json['next']
        return list_response

    @property
    def usergrouplist(self):
        path = 'https://app.drchrono.com/api/user_groups'
        list_response = []
        while path:
            data = requests.get(path, headers={'Authorization': 'Bearer ' + self.api_key})
            data_json = data.json()
            list_response.extend(data_json['results'])
            path = data_json['next']
        return list_response

    def user_single(self, user_id):
        path = 'https://app.drchrono.com/api/users/{}'.format(user_id)
        try: 
            data = requests.get(path, headers={'Authorization': 'Bearer ' + self.api_key})
            data_json = data.json()
            return data_json
        except Exception as e:
            print(e)

    def usergrouplist_single(self, group_id):
        path = 'https://app.drchrono.com/api/user_groups/{}'.format(group_id)
        try: 
            data = requests.get(path, headers={'Authorization': 'Bearer ' + self.api_key})
            data_json = data.json()
            return data_json
        except Exception as e:
            print(e)



