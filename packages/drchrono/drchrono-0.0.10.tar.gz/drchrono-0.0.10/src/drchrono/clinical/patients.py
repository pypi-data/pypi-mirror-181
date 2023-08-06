import requests
class PATIENTS():

    def __init__(self, api_key, patient_id=None, fake_count=None, verbose_true=None, **kwargs):
        self.patient_id = patient_id
        self.fake_count = fake_count
        self.verbose_true = verbose_true
        assert isinstance(api_key, str), 'You must provide a valid API Key'
        self.api_key = api_key

    # @property
    def patientlist(self, verbose_true):
        print('Key sent: ', self.api_key)

        if verbose_true == True:
            print('Verbose mode is on')
            path = 'https://drchrono.com/api/patients?verbose=true'
        else:
            print('Verbose mode is off')
            path = 'https://drchrono.com/api/patients'
        
        list_response = []
        while path:
            data = requests.get(path, headers={'Authorization': 'Bearer ' + self.api_key})
            data_json = data.json()
            list_response.extend(data_json['results'])
            path = data_json['next']
        return list_response

    def patient_single(self, patient_id, verbose_true):
        if verbose_true == True:
            print('Verbose mode is on')
            path = 'https://drchrono.com/api/patients?verbose=true'
        else:
            print('Verbose mode is off')
            path = 'https://drchrono.com/api/patients'
        print('path: ', path)
        try: 
            data = requests.get(path, headers={'Authorization': 'Bearer ' + self.api_key})
            data_json = data.json()
            return data_json
        except Exception as e:
            print(e)

    def patient_summary_read(self, patient_id):
        path = 'https://drchrono.com/api/patients_summary/{}'.format(patient_id)
        try: 
            data = requests.get(path, headers={'Authorization': 'Bearer ' + self.api_key})
            if data == 200:
                data_json = data.json()
                return data_json
            else:
                print('Error: {}'.format(data))
        except Exception as e:
            print(e)

    def patient_ccda(self, patient_id):
        path = 'https://drchrono.com/api/patients/{}/ccda'.format(patient_id)
        try: 
            data = requests.get(path, headers={'Authorization': 'Bearer ' + self.api_key})
            if data == 200:
                data_json = data.json()
                return data_json
            else:
                print('Error: {}'.format(data))
        except Exception as e:
            print(e)

    def patient_onpatient(self, patient_id):
        path = 'https://drchrono.com/api/patients/{}/onpatient_access'.format(patient_id)
        try: 
            data = requests.get(path, headers={'Authorization': 'Bearer ' + self.api_key})
            if data == 200:
                data_json = data.json()
                return data_json
            else:
                print('Error: {}'.format(data))
        except Exception as e:
            print(e)