import requests

class DOCTORS():

    """
    https://app.drchrono.com/api-docs/#tag/Administrative/operation/doctors_list

    """

    def __init__(self, api_key, doctor_id=None):
        self.doctor_id = doctor_id
        assert isinstance(api_key, str), 'You must provide a valid API Key'
        self.api_key = api_key

    @property
    def doctorlist(self):
        path = 'https://app.drchrono.com/api/doctors'
        list_response = []

        while path:
            data = requests.get(path, headers={'Authorization': 'Bearer ' + self.api_key})
            data_json = data.json()
            list_response.extend(data_json['results'])
            path = data_json['next'] 
        
        return list_response
   
    def doctor_single(self, doctor_id):
        path = 'https://app.drchrono.com/api/doctors/{}'.format(doctor_id)
        try: 
            data = requests.get(path, headers={'Authorization': 'Bearer ' + self.api_key})
            data_json = data.json()
            return data_json
        except Exception as e:
            print(e)





