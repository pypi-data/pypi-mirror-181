from . import session

class USERS(object):

    def __init__(self, user_id=None, group_id=None, fake_count=1):
        self.user_id = user_id
        self.group_id = group_id
        self.fake_count = fake_count

    @staticmethod
    def userlist():
        path = 'https://app.drchrono.com/api/users'
        list_response = []
        while path:
            data = session.get(path)
            data_json = data.json()
            list_response.extend(data_json['results'])
            path = data_json['next']
        return list_response

    @staticmethod
    def usergrouplist():
        path = 'https://app.drchrono.com/api/user_groups'
        list_response = []
        while path:
            data = session.get(path)
            data_json = data.json()
            list_response.extend(data_json['results'])
            path = data_json['next']
        return list_response

    @classmethod
    def user_single(cls, user_id):
        path = 'https://app.drchrono.com/api/users/{}'.format(user_id)
        try: 
            data = session.get(path)
            data_json = data.json()
            return data_json
        except Exception as e:
            print(e)

    @classmethod
    def usergrouplist_single(cls, group_id):
        path = 'https://app.drchrono.com/api/user_groups/{}'.format(group_id)
        try: 
            data = session.get(path)
            data_json = data.json()
            return data_json
        except Exception as e:
            print(e)



