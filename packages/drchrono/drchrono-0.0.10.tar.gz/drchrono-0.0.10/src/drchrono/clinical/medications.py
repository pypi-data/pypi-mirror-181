import requests

class MEDICATIONS():

    def __init__(self, api_key, patient_id=None, medication_id=None, **kwargs):
        self.patient_id = patient_id
        self.medication_id = medication_id
        assert isinstance(api_key, str), 'You must provide a valid API Key'
        self.api_key = api_key

    @property
    def medicationlist(self):
        path = 'https://app.drchrono.com/api/medications'
        list_response = []
        while path:
            data = requests.get(path, headers={'Authorization': 'Bearer ' + self.api_key})
            data_json = data.json()
            list_response.extend(data_json['results'])
            path = data_json['next']
        return list_response

    def medication_patient(self, patient_id):
        path = "https://app.drchrono.com/api/medications?patient=" + patient_id 
        try: 
            data = requests.get(path, headers={'Authorization': 'Bearer ' + self.api_key})
            data_json = data.json()
            return data_json
        except Exception as e:
            print(e)

    def medication_single(self, medication_id):
        path = 'https://app.drchrono.com/api/medications/{}'.format(medication_id)
        try: 
            data = requests.get(path, headers={'Authorization': 'Bearer ' + self.api_key})
            data_json = data.json()
            return data_json
        except Exception as e:
            print(e)