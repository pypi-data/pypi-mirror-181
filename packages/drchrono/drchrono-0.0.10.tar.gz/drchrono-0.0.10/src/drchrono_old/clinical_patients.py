from . import session

class PATIENTS(object):

    def __init__(self, patient_id=None, fake_count=None, **kwargs):
        self.patient_id = patient_id
        self.fake_count = fake_count

    @staticmethod
    def patientlist():
        path = 'https://drchrono.com/api/patients'
        list_response = []
        while path:
            data = session.get(path)
            data_json = data.json()
            list_response.extend(data_json['results'])
            path = data_json['next']
        return list_response

    @classmethod
    def patient_single(cls, patient_id):
        path = 'https://drchrono.com/api/patients/{}'.format(patient_id)
        print('path: ', path)
        try: 
            data = session.get(path)
            if data == 200:
                data_json = data.json()
                return data_json
            else:
                print('Error: {}'.format(data))
        except Exception as e:
            print(e)

    @classmethod
    def patient_summary_read(cls, patient_id):
        path = 'https://drchrono.com/api/patients_summary/{}'.format(patient_id)
        try: 
            data = session.get(path)
            if data == 200:
                data_json = data.json()
                return data_json
            else:
                print('Error: {}'.format(data))
        except Exception as e:
            print(e)

    @classmethod
    def patient_ccda(cls, patient_id):
        path = 'https://drchrono.com/api/patients/{}/ccda'.format(patient_id)
        try: 
            data = session.get(path)
            if data == 200:
                data_json = data.json()
                return data_json
            else:
                print('Error: {}'.format(data))
        except Exception as e:
            print(e)

    @classmethod
    def patient_onpatient(cls, patient_id):
        path = 'https://drchrono.com/api/patients/{}/onpatient_access'.format(patient_id)
        try: 
            data = session.get(path)
            if data == 200:
                data_json = data.json()
                return data_json
            else:
                print('Error: {}'.format(data))
        except Exception as e:
            print(e)